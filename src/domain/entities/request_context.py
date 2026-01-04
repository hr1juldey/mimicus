"""RequestContext domain entity representing an incoming HTTP request."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class RequestContext:
    """Context of an incoming HTTP request."""

    request_method: str
    request_path: str
    request_headers: Dict[str, str] = field(default_factory=dict)
    request_query_params: Dict[str, str] = field(default_factory=dict)
    request_body: Optional[str] = None
    request_json: Optional[Dict[str, Any]] = None
    request_path_params: Dict[str, str] = field(default_factory=dict)

    def get_request_header(self, header_name: str) -> Optional[str]:
        """Get header value case-insensitively."""
        for key, value in self.request_headers.items():
            if key.lower() == header_name.lower():
                return value
        return None

    def has_json_body(self) -> bool:
        """Check if request has JSON body."""
        return self.request_json is not None

    def __str__(self) -> str:
        """String representation of request context."""
        return f"{self.request_method} {self.request_path}"
