"""Repository interface for request log entities."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.domain.entities.request_log import RequestLog


class RequestLogRepository(ABC):
    """Abstract repository interface for request logs."""

    @abstractmethod
    async def create(self, request_log: RequestLog) -> RequestLog:
        """Create a new request log."""
        pass

    @abstractmethod
    async def get_by_id(self, log_id: str) -> Optional[RequestLog]:
        """Get a request log by ID."""
        pass

    @abstractmethod
    async def get_by_session(
        self, session_id: str, limit: int = 50
    ) -> List[RequestLog]:
        """Get request logs by session ID."""
        pass

    @abstractmethod
    async def get_by_mock(self, mock_id: str, limit: int = 50) -> List[RequestLog]:
        """Get request logs by mock ID."""
        pass

    @abstractmethod
    async def get_recent(self, limit: int = 50) -> List[RequestLog]:
        """Get recent request logs."""
        pass


class InMemoryRequestLogRepository(RequestLogRepository):
    """In-memory implementation of RequestLogRepository."""

    def __init__(self):
        """Initialize in-memory storage."""
        self._logs: Dict[str, RequestLog] = {}

    async def create(self, request_log: RequestLog) -> RequestLog:
        """Create a new request log."""
        self._logs[request_log.log_id] = request_log
        return request_log

    async def get_by_id(self, log_id: str) -> Optional[RequestLog]:
        """Get a request log by ID."""
        return self._logs.get(log_id)

    async def get_by_session(
        self, session_id: str, limit: int = 50
    ) -> List[RequestLog]:
        """Get request logs by session ID."""
        logs = [log for log in self._logs.values() if log.session_id == session_id]
        # Sort by creation time, most recent first
        logs.sort(key=lambda x: x.created_at, reverse=True)
        return logs[:limit]

    async def get_by_mock(self, mock_id: str, limit: int = 50) -> List[RequestLog]:
        """Get request logs by mock ID."""
        logs = [log for log in self._logs.values() if log.matched_mock_id == mock_id]
        # Sort by creation time, most recent first
        logs.sort(key=lambda x: x.created_at, reverse=True)
        return logs[:limit]

    async def get_recent(self, limit: int = 50) -> List[RequestLog]:
        """Get recent request logs."""
        logs = list(self._logs.values())
        # Sort by creation time, most recent first
        logs.sort(key=lambda x: x.created_at, reverse=True)
        return logs[:limit]
