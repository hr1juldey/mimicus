"""Use case for deleting state."""

from typing import Optional
from src.domain.services.state_service import StateService


class DeleteStateUseCase:
    """Delete state by key and session."""

    def __init__(self, state_service: StateService):
        """Initialize use case."""
        self.state_service = state_service

    async def execute(
        self, state_key: str, session_id: Optional[str] = None
    ) -> bool:
        """Delete state and return True if deleted."""
        return await self.state_service.delete_state(state_key, session_id)
