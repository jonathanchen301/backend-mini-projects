from fastapi import FastAPI
from app.config import settings
from app.routers import system
from app.routers.v1 import sample

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(system.router)
app.include_router(sample.router, prefix=settings.api_v1_prefix)