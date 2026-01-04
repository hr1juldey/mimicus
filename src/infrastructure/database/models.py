"""SQLModel database models for persistence."""

from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class MockDefinitionModel(SQLModel, table=True):
    """Database model for storing mock definitions."""

    __tablename__ = "mock_definitions"

    mock_id: str = Field(primary_key=True)
    mock_name: str
    mock_priority: int = Field(default=100)
    mock_enabled: bool = Field(default=True)
    mock_mode: str = Field(default="mock")

    # Store match and response configurations as JSON strings
    mock_match_json: str
    mock_response_json: str

    # Optional state and hooks configuration
    mock_state_json: Optional[str] = None
    mock_hooks_json: Optional[str] = None

    # Upstream URL for proxy mode
    upstream_url: Optional[str] = None
    timeout_seconds: int = Field(default=10)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""

        validate_assignment = True
