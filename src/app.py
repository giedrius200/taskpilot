from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Form
from sqlmodel import select
from sqlmodel import Session
from typing import List
from contextlib import asynccontextmanager

from . import models, db, auth, schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize DB on startup
    db.init_db()
    yield


app = FastAPI(title="Task Manager", lifespan=lifespan)


def notify_user(task_id: int):
    # Simulate sending a notification (background task example)
    print(f"Notify about task {task_id}")


@app.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate):
    with Session(db.engine) as session:
        existing = session.exec(select(models.User).where(models.User.username == user.username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="username taken")
        u = models.User(username=user.username, hashed_password=auth.hash_password(user.password))
        session.add(u)
        session.commit()
        token = auth.create_access_token(u.username)
        return {"access_token": token, "token_type": "bearer"}


@app.post("/login", response_model=schemas.Token)
def login(username: str = Form(None), password: str = Form(None), user: schemas.UserCreate | None = None):
    """
    Accept either form-encoded username/password (used by Swagger UI OAuth2 password flow)
    or JSON body matching schemas.UserCreate (used by tests / API clients).
    """
    # prefer form data if provided
    if username is not None and password is not None:
        uname, pwd = username, password
    elif user is not None:
        uname, pwd = user.username, user.password
    else:
        raise HTTPException(status_code=400, detail="Missing credentials")

    with Session(db.engine) as session:
        db_user = session.exec(select(models.User).where(models.User.username == uname)).first()
        if not db_user or not auth.verify_password(pwd, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="invalid credentials")
        token = auth.create_access_token(db_user.username)
        return {"access_token": token, "token_type": "bearer"}


@app.post("/tasks", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, background_tasks: BackgroundTasks, username: str = Depends(auth.get_current_user)):
    with Session(db.engine) as session:
        user = session.exec(select(models.User).where(models.User.username == username)).first()
        if not user:
            raise HTTPException(status_code=404)
        t = models.Task(title=task.title, description=task.description, owner_id=user.id)
        session.add(t)
        session.commit()
        session.refresh(t)
        background_tasks.add_task(notify_user, t.id)
        return t


@app.get("/tasks", response_model=List[schemas.TaskRead])
def list_tasks(username: str = Depends(auth.get_current_user)):
    with Session(db.engine) as session:
        user = session.exec(select(models.User).where(models.User.username == username)).first()
        if not user:
            return []
        tasks = session.exec(select(models.Task).where(models.Task.owner_id == user.id)).all()
        return tasks
