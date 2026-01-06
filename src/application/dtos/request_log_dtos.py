"""Data Transfer Objects for request log operations."""

from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, Field


class RequestLogDTO(BaseModel):
    """DTO for request log in API responses."""

    log_id: str
    request_method: str
    request_path: str
    request_headers: Dict[str, str]
    request_body: Optional[str]
    matched_mock_id: Optional[str]
    template_context: Optional[Dict]
    response_status: int
    response_body: Optional[str]
    client_ip: Optional[str]
    session_id: Optional[str]
    created_at: datetime


class RequestLogCreateDTO(BaseModel):
    """DTO for creating a request log."""

    request_method: str = Field(..., description="HTTP method of the request")
    request_path: str = Field(..., description="Path of the request")
    request_headers: Dict[str, str] = Field(default_factory=dict)
    request_body: Optional[str] = None
    matched_mock_id: Optional[str] = None
    response_status: int = Field(default=200, description="Response status code")
    response_body: Optional[str] = None
    client_ip: Optional[str] = None
    session_id: Optional[str] = None


class RequestLogListResponseDTO(BaseModel):
    """DTO for list of request logs."""

    logs: list[RequestLogDTO]
    count: int
