from fastapi import APIRouter
from app.config import settings

router = APIRouter(
    tags = ["System"]
)

@router.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/info")
def get_info() -> dict[str, str | bool]:
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
    }