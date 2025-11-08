from fastapi import FastAPI
from routers import items, files

app = FastAPI(
    title="Items and Files API",
    description="CRUD API for items + file upload",
    version="1.0.0"
)

app.include_router(items.router)
app.include_router(files.router)

