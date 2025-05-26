# app/schemas.py
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Todo(BaseModel):
    id: str
    title: str
    completed: bool
