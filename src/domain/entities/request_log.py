"""Request log entity for audit logging."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from src.domain.entities.request_context import RequestContext


@dataclass
class RequestLog:
    """Domain entity representing a logged request."""

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

    @classmethod
    def from_request_context(
        cls,
        log_id: str,
        request_context: RequestContext,
        matched_mock_id: Optional[str] = None,
        response_status: int = 200,
        response_body: Optional[str] = None,
        created_at: datetime = None,
    ):
        """Create a RequestLog from a RequestContext."""
        if created_at is None:
            from datetime import datetime

            created_at = datetime.now()

        return cls(
            log_id=log_id,
            request_method=request_context.request_method,
            request_path=request_context.request_path,
            request_headers=request_context.request_headers,
            request_body=request_context.request_body,
            matched_mock_id=matched_mock_id,
            template_context=None,  # Will be populated during response generation
            response_status=response_status,
            response_body=response_body,
            client_ip=request_context.client_ip,
            session_id=request_context.session_id,
            created_at=created_at,
        )
