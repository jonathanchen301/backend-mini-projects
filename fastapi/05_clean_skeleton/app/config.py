from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Clean Skeleton"
    debug: bool = False
    environment: str = "development"
    database_url: str = "sqlite:///./test.db"
    jwt_secret: str = "dev-secret-key"
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()