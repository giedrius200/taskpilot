import pytest
from fastapi.testclient import TestClient

from src.app import app
from src import db


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    # use a temporary sqlite file for tests
    db_url = f"sqlite:///{tmp_path / 'test.db'}"
    monkeypatch.setattr("src.db.DATABASE_URL", db_url)
    # re-create engine with new url
    from sqlmodel import create_engine
    db.engine = create_engine(db_url, connect_args={"check_same_thread": False})
    db.init_db()


def test_register_login_and_task_flow():
    client = TestClient(app)

    # register
    r = client.post("/register", json={"username": "alice", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    # login
    r2 = client.post("/login", json={"username": "alice", "password": "secret"})
    assert r2.status_code == 200
    token2 = r2.json()["access_token"]
    assert token2

    headers = {"Authorization": f"Bearer {token2}"}

    # create a task
    r3 = client.post("/tasks", json={"title": "Test Task", "description": "demo"}, headers=headers)
    assert r3.status_code == 200
    task = r3.json()
    assert task["title"] == "Test Task"

    # list tasks
    r4 = client.get("/tasks", headers=headers)
    assert r4.status_code == 200
    tasks = r4.json()
    assert isinstance(tasks, list)
    assert any(t["title"] == "Test Task" for t in tasks)
