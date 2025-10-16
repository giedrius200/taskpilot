from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True
