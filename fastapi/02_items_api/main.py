from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import uuid

class ItemRequest(BaseModel):
    name: str
    price: float
    tags: list[str] = Field(default = [])

class Item(BaseModel):
    id: str
    name: str
    price: float
    tags: list[str] = Field(default = [])

memory = {}

app = FastAPI()

@app.post("/items", response_model=Item)
def create_item(item_request: ItemRequest):
    id = str(uuid.uuid4())
    item = Item(
        id = id,
        **item_request.model_dump()
    )
    memory[id] = item
    return item

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    if item_id not in memory:
        raise HTTPException(status_code=404, detail="Item not found")
    return memory[item_id]