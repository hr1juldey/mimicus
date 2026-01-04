"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables
    )

    # Database configuration
    config_database_url: str = "sqlite+aiosqlite:///./mimicus.db"

    # API configuration
    config_api_key: str = "dev-secret-key"
    config_mock_mode: str = "enabled"

    # Server configuration
    mock_server_host: str = "0.0.0.0"
    mock_server_port: int = 18000
    mock_server_reload: bool = False

    # Logging configuration
    mock_log_level: str = "INFO"
    mock_log_format: str = "json"

    # Optional upstream for proxy mode
    config_upstream_url: Optional[str] = None
    timeout_seconds: int = 10

    # JWT configuration
    config_jwt_secret: str = "change-me-in-production"
    config_jwt_algorithm: str = "HS256"
    config_jwt_expiration_minutes: int = 60


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
