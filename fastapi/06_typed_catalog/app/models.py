from enum import Enum
from pydantic import BaseModel, constr, Field, ConfigDict
from typing import Optional

class Category(str, Enum):
    ELECTRONICS = "electronics"
    BOOKS = "books"
    CLOTHING = "clothing"
    FOOD = "food"

class ItemCreate(BaseModel):
    name: constr(min_length=3, max_length=100) = Field(..., example="Pencil")
    description: Optional[str] = Field(example = "A writing instrument")
    price: float = Field(..., gt=0, example = 1.00)
    category: Category = Field(..., example = Category.ELECTRONICS)
    tags: list[str] = Field(default = [], example = ["Writing", "Office"])

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Pencil",
                    "description": "A writing instrument",
                    "price": 1.00,
                    "category": "electronics",
                    "tags": ["Writing", "Office"]
                }
            ]
        }
    )

class Item(ItemCreate):
    item_id: int = Field(..., example = 1)
    internal_notes: str = Field(example = "This is a pencil")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "item_id": 1,
                    "name": "Pencil",
                    "description": "A writing instrument",
                    "price": 1.00,
                    "category": "electronics",
                    "tags": ["Writing", "Office"]
                }
            ]
        }
    )