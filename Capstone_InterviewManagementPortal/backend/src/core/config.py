"""Application configuration loaded from environment variables."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the backend service.

    Values are loaded from process environment variables and the optional
    ``.env`` file. Required values must be present before application startup
    so configuration errors surface early.

    Attributes:
        PROJECT_NAME: Display name used in generated API documentation.
        API_V1_STR: Prefix applied to versioned API routes.
        MONGODB_URL: MongoDB connection string.
        DATABASE_NAME: MongoDB database selected by the application.
        ENVIRONMENT: Deployment environment label returned by health checks.
        LOG_LEVEL: Standard Python logging level name.
    """

    PROJECT_NAME: str = "Interview Management Portal"
    API_V1_STR: str = "/api/v1"
    MONGODB_URL: str
    DATABASE_NAME: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
