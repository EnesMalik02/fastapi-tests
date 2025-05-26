# main.py
from fastapi import FastAPI

app = FastAPI()


#http://127.0.0.1:8000/
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


#http://127.0.0.1:8000/items/42?q=sorgu metni
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

from pydantic import BaseModel
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"created": item}
