"""
Application settings using pydantic-settings for environment variable management.
This removes hardcoded values and enables proper configuration management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Security
    SECRET_KEY: str = (
        "your-secret-key-change-in-production"  # Default for dev, MUST be overridden in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./government_spending.db"

    # Note: CORS_ORIGINS is NOT defined here to avoid pydantic-settings JSON parsing
    # It will be read directly from os.getenv() in main.py

    # API
    API_TITLE: str = "Government Spending Tracker"
    API_VERSION: str = "1.0.0"


# Global settings instance
settings = Settings()
