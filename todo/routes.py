# app/routes.py
from fastapi import APIRouter, HTTPException, status
from typing import List

from .models import (
    create_todo, get_all_todos, get_todo,
    update_todo, delete_todo
)
from .schemas import TodoCreate, TodoUpdate, Todo

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create(item: TodoCreate):
    return create_todo(item.title)

@router.get("/", response_model=List[Todo])
async def list_all():
    return get_all_todos()

@router.get("/{todo_id}", response_model=Todo)
async def read_one(todo_id: str):
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=Todo)
async def update(todo_id: str, item: TodoUpdate):
    todo = update_todo(todo_id, item.title, item.completed)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(todo_id: str):
    success = delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return
