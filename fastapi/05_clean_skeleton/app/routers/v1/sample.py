from fastapi import APIRouter, Depends, HTTPException
from app.models.sample import SampleItem
from app.services.sample_service import get_sample_items, get_sample_item, memory
from app.deps.common import get_current_environment

router = APIRouter(
    prefix = "/sample",
    tags = ["Sample v1"]
)

# This one is just demoing the Depends, it doesn't have any real logic.
@router.get("/", 
response_model=list[SampleItem],
summary="Get all sample items",
description="Get all sample items from the database")
def get_items(curr_env: str = Depends(get_current_environment)) -> list[SampleItem]:
    print(f"Current environment: {curr_env}")
    return get_sample_items()

@router.get("/{item_id}",
response_model=SampleItem,
summary="Get a sample item",
description="Get a sample item from the database")
def get_item(item_id: int) -> SampleItem:
    item = get_sample_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item