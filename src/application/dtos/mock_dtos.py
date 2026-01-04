"""Data Transfer Objects for mock operations."""

from typing import Dict, Optional, Union, Any
from pydantic import BaseModel, Field, ConfigDict


class MatchCriteriaDTO(BaseModel):
    """DTO for match criteria."""

    match_method: str = Field(..., description="HTTP method: GET, POST, etc")
    match_path: str = Field(..., description="Path pattern: /api/users or /api/users/{id}")
    match_headers: Optional[Dict[str, str]] = None
    match_query: Optional[Dict[str, str]] = None
    match_body: Optional[Dict[str, str]] = None
    match_content_type: Optional[str] = None


class ResponseConfigDTO(BaseModel):
    """DTO for response configuration."""

    response_status: int = Field(default=200, description="HTTP status code")
    response_headers: Dict[str, str] = Field(default_factory=dict)
    response_body: Union[str, Dict[str, Any]] = Field(
        default="", description="Response body (static or template)"
    )
    response_delay_ms: int = Field(default=0, description="Delay in milliseconds")
    is_template: bool = Field(default=False, description="Whether body is Jinja2 template")


class CreateMockDTO(BaseModel):
    """DTO for creating a new mock."""

    mock_name: str = Field(..., description="Name of the mock")
    mock_priority: int = Field(default=100, description="Priority (higher = earlier)")
    mock_enabled: bool = Field(default=True)
    mock_mode: str = Field(default="mock", description="Mode: mock, proxy, etc")
    match_method: str
    match_path: str
    match_headers: Optional[Dict[str, str]] = None
    match_query: Optional[Dict[str, str]] = None
    response_status: int = 200
    response_headers: Dict[str, str] = Field(default_factory=dict)
    response_body: Union[str, Dict[str, Any]] = ""
    response_delay_ms: int = 0
    is_template: bool = False
    upstream_url: Optional[str] = None
    timeout_seconds: int = 10


class UpdateMockDTO(BaseModel):
    """DTO for updating a mock."""

    mock_name: Optional[str] = None
    mock_priority: Optional[int] = None
    mock_enabled: Optional[bool] = None
    response_status: Optional[int] = None
    response_headers: Optional[Dict[str, str]] = None
    response_body: Optional[Union[str, Dict[str, Any]]] = None
    response_delay_ms: Optional[int] = None
    is_template: Optional[bool] = None
    upstream_url: Optional[str] = None
    timeout_seconds: Optional[int] = None


class MockResponseDTO(BaseModel):
    """DTO for mock in API responses."""

    model_config = ConfigDict(from_attributes=True)

    mock_id: str
    mock_name: str
    mock_priority: int
    mock_enabled: bool
    mock_mode: str
    response_status: int
    response_headers: Dict[str, str]
    response_body: Union[str, Dict[str, Any]]
    response_delay_ms: int
    is_template: bool
    upstream_url: Optional[str]


class MockListResponseDTO(BaseModel):
    """DTO for list of mocks."""

    mocks: list[MockResponseDTO]
    count: int


class ErrorResponseDTO(BaseModel):
    """DTO for error responses."""

    error: str
    detail: Optional[str] = None


class HealthResponseDTO(BaseModel):
    """DTO for health check."""

    status: str
    service: str
    version: str
