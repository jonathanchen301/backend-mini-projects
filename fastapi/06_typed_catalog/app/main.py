from fastapi import FastAPI, Request, Query, Path
from fastapi.responses import JSONResponse
from app.exceptions import DomainError
from app.models import Item, ItemCreate, Category

items_db = {}
next_id = 1

app = FastAPI()

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code = 422,
        content = {"error": exc.__class__.__name__, "message": exc.message, "field": exc.field}
    )

@app.post("/items",
status_code=201,
response_model=Item,
response_model_exclude={"internal_notes"})
def create_item(item_request: ItemCreate) -> Item:
    global next_id
    tags = [tag.lower() for tag in item_request.tags]
    tags = list(set(tags))

    item = Item(
        item_id = next_id,
        name = item_request.name,
        description = item_request.description,
        price = item_request.price,
        category = item_request.category,
        tags = tags,
        internal_notes = f"Created item {item_request.name}"
    )
    items_db[next_id] = item
    next_id += 1
    return item

@app.get("/items", 
response_model=list[Item],
response_model_exclude={"internal_notes"})
def get_items(category: Category | None = None, min_price: float = Query(default=0, ge=0), max_price: float | None = Query(default=None, gt=0)) -> list[Item]:
    items = list(items_db.values())
    if category:
        items = [item for item in items if item.category == category]
    items = [item for item in items if item.price >= min_price]
    if max_price:
        items = [item for item in items if item.price <= max_price]
    return items

@app.get("/items/{item_id}",
response_model=Item,
response_model_exclude={"internal_notes"})
def get_item(item_id: int = Path(..., gt=0)) -> Item:
    item = items_db.get(item_id)
    if not item:
        raise DomainError("Item not found", field="item_id")
    return item