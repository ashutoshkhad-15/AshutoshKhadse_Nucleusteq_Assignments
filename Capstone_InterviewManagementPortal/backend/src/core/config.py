import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Interview Management Portal"
    API_V1_STR: str = "/api/v1"
    MONGODB_URL: str
    DATABASE_NAME: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()