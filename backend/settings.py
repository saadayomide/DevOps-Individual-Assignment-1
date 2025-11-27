"""
Application settings using pydantic-settings for environment variable management.
This removes hardcoded values and enables proper configuration management.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Security
    SECRET_KEY: str = (
        "your-secret-key-change-in-production"  # Default for dev, MUST be overridden in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./government_spending.db"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # API
    API_TITLE: str = "Government Spending Tracker"
    API_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
