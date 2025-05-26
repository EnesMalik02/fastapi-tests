# app/models.py
from typing import Dict
from uuid import uuid4

# Basit in-memory depolama
# key: todo_id, value: {"id":..., "title":..., "completed":...}
TODOS: Dict[str, dict] = {}

def create_todo(title: str) -> dict:
    todo_id = str(uuid4())
    TODOS[todo_id] = {"id": todo_id, "title": title, "completed": False}
    return TODOS[todo_id]

def get_all_todos() -> list[dict]:
    return list(TODOS.values())

def get_todo(todo_id: str) -> dict | None:
    return TODOS.get(todo_id)

def update_todo(todo_id: str, title: str | None, completed: bool | None) -> dict | None:
    todo = TODOS.get(todo_id)
    if not todo:
        return None
    if title is not None:
        todo["title"] = title
    if completed is not None:
        todo["completed"] = completed
    return todo

def delete_todo(todo_id: str) -> bool:
    return TODOS.pop(todo_id, None) is not None
