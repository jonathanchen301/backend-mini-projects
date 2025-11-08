from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import uuid

memory = {}

class ItemRequest(BaseModel):
    name: str
    price: float
    tags: list[str] = Field(default = [])

    class ConfigDict:
        example = {
            "name": "Pencil",
            "price": 1.00,
            "tags": ["Items"]
        }

class Item(BaseModel):
    item_id: str
    name: str
    price: float
    tags: list[str] = Field(default = [])

    class ConfigDict:
        example = {
            "item_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Pencil",
            "price": 1.00,
            "tags": ["Items"]
        }

router = APIRouter(
    prefix = "/items",
    tags = ["items"],
)

@router.post("/", response_model=Item, summary="Create an item", description="Assign an id to the item and store it in the database")
def create_item(item_request: ItemRequest):
    item_id = str(uuid.uuid4())
    item = Item(
        item_id = item_id,
        **item_request.model_dump()
    )
    memory[item_id] = item
    return item

@router.get("/{item_id}", response_model=Item, summary="Get an item by id", description="Get an item by id from the database")
def get_item(item_id: str):
    if item_id not in memory:
        raise HTTPException(status_code=404, detail="Item not found")
    return memory[item_id]

@router.put("/{item_id}", response_model=Item, summary="Update an item by id", description="Update an item by id from the database")
def update_item(item_id: str,item_request: ItemRequest):
    if item_id not in memory:
        raise HTTPException(status_code=404, detail="Item not found")
    memory[item_id] = Item(
        item_id = item_id,
        **item_request.model_dump(),
    )
    return memory[item_id]

@router.delete("/{item_id}", summary="Delete an item by id", description="Delete an item by id from the database")
def delete_item(item_id: str):
    if item_id not in memory:
        raise HTTPException(status_code=404, detail="Item not found")
    del memory[item_id]
    return {"message": "Item deleted successfully"}