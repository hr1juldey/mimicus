"""Use case for incrementing state counter."""

from typing import Optional
from src.domain.services.state_service import StateService


class IncrementStateUseCase:
    """Atomically increment state counter."""

    def __init__(self, state_service: StateService):
        """Initialize use case."""
        self.state_service = state_service

    async def execute(
        self,
        state_key: str,
        session_id: Optional[str] = None,
        delta: int = 1,
    ) -> int:
        """Increment counter and return new value."""
        return await self.state_service.increment_counter(
            state_key, session_id, delta
        )
