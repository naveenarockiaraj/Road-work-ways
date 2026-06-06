from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Road Work Ways"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/roadworks_db"

    # JWT
    SECRET_KEY: str = "change-me-in-production-use-at-least-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # First superuser
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@roadworkways.in"
    FIRST_SUPERUSER_PASSWORD: str = "Admin@123456"
    FIRST_SUPERUSER_FULLNAME: str = "System Administrator"

    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}


settings = Settings()
