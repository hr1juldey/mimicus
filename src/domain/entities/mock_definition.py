"""MockDefinition domain entity representing a mock configuration."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Union
from enum import Enum


class MockMode(str, Enum):
    """Mock operation modes."""

    MOCK = "mock"
    PROXY = "proxy"
    PROXY_WITH_FALLBACK = "proxy-with-fallback"
    PASSTHROUGH = "passthrough"


@dataclass
class MatchCriteria:
    """Request matching criteria."""

    match_method: str  # GET, POST, PUT, DELETE, PATCH, etc.
    match_path: str  # /api/users or /api/users/{id}
    match_headers: Optional[Dict[str, str]] = None
    match_query: Optional[Dict[str, str]] = None
    match_body: Optional[Dict[str, str]] = None
    match_content_type: Optional[str] = None


@dataclass
class ResponseConfig:
    """Response configuration."""

    response_status: int = 200
    response_headers: Dict[str, str] = field(default_factory=dict)
    response_body: Union[str, Dict] = ""
    response_delay_ms: int = 0
    is_template: bool = False
    error_rate: int = 0
    error_status_code: int = 500
    error_body: str = ""


@dataclass
class MockDefinition:
    """Domain entity representing a complete mock definition."""

    mock_id: str
    mock_name: str
    mock_priority: int = 100
    mock_enabled: bool = True
    mock_mode: str = "mock"
    mock_match: MatchCriteria = field(default_factory=lambda: MatchCriteria("GET", "/"))
    mock_response: ResponseConfig = field(default_factory=ResponseConfig)
    mock_state: Optional[Dict[str, str]] = None
    upstream_url: Optional[str] = None
    timeout_seconds: int = 10

    def is_active(self) -> bool:
        """Check if mock is enabled and active."""
        return self.mock_enabled

    def get_match_path(self) -> str:
        """Get path template for matching."""
        return self.mock_match.match_path

    def get_match_method(self) -> str:
        """Get HTTP method for matching."""
        return self.mock_match.match_method
