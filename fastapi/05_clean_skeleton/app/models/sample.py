from pydantic import BaseModel

class SampleItemCreate(BaseModel):
    name: str
    description: str

class SampleItem(SampleItemCreate):
    item_id: int