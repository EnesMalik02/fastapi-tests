# app/main.py
from fastapi import FastAPI
from todo.routes import router as todo_router

app = FastAPI(
    title="Simple ToDo API",
    description="In-memory ToDo list example with FastAPI",
    version="0.1.0"
)

#uvicorn todo.main:app --reload
app.include_router(todo_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Simple ToDo API"}
