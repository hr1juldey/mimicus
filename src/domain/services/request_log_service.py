"""Request logging service for audit logging."""

import uuid
from datetime import datetime
from typing import List, Optional
from src.domain.entities.request_log import RequestLog
from src.domain.repositories.request_log_repository import RequestLogRepository
from src.domain.entities.request_context import RequestContext


class RequestLogService:
    """Service for managing request logs."""

    def __init__(self, repository: RequestLogRepository):
        """Initialize the service with a repository."""
        self.repository = repository

    async def log_request(
        self,
        request_context: RequestContext,
        matched_mock_id: Optional[str] = None,
        response_status: int = 200,
        response_body: Optional[str] = None,
    ) -> RequestLog:
        """Log an incoming request."""
        log_id = str(uuid.uuid4())
        request_log = RequestLog.from_request_context(
            log_id=log_id,
            request_context=request_context,
            matched_mock_id=matched_mock_id,
            response_status=response_status,
            response_body=response_body,
            created_at=datetime.now(),
        )
        return await self.repository.create(request_log)

    async def get_log_by_id(self, log_id: str) -> Optional[RequestLog]:
        """Get a request log by ID."""
        return await self.repository.get_by_id(log_id)

    async def get_logs_by_session(
        self, session_id: str, limit: int = 50
    ) -> List[RequestLog]:
        """Get request logs by session ID."""
        return await self.repository.get_by_session(session_id, limit)

    async def get_logs_by_mock(self, mock_id: str, limit: int = 50) -> List[RequestLog]:
        """Get request logs by mock ID."""
        return await self.repository.get_by_mock(mock_id, limit)

    async def get_recent_logs(self, limit: int = 50) -> List[RequestLog]:
        """Get recent request logs."""
        return await self.repository.get_recent(limit)
