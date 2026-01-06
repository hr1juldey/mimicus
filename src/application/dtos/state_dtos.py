"""Data Transfer Objects for state operations."""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class StateDTO(BaseModel):
    """DTO for state in API responses."""

    model_config = ConfigDict(from_attributes=True)

    state_key: str = Field(..., description="State key")
    state_value: str = Field(..., description="State value")
    session_id: Optional[str] = Field(None, description="Session ID")
    mock_id: Optional[str] = Field(None, description="Mock ID")
    client_ip: Optional[str] = Field(None, description="Client IP")


class SetStateDTO(BaseModel):
    """DTO for setting state."""

    state_key: str = Field(..., description="State key to set")
    state_value: str = Field(..., description="State value to set")


class GetStateDTO(BaseModel):
    """DTO for getting state."""

    state_key: str = Field(..., description="State key to retrieve")


class StateListDTO(BaseModel):
    """DTO for list of state items."""

    states: list[StateDTO] = Field(default_factory=list)
    count: int = Field(default=0, description="Number of states")
