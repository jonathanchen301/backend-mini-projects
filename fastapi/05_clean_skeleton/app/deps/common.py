from app.config import settings

def get_current_environment() -> str:
    return settings.environment