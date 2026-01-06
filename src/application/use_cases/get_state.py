"""Use case for retrieving state."""

from typing import Optional
from src.domain.services.state_service import StateService


class GetStateUseCase:
    """Get state by key and session."""

    def __init__(self, state_service: StateService):
        """Initialize use case."""
        self.state_service = state_service

    async def execute(
        self, state_key: str, session_id: Optional[str] = None
    ) -> Optional[str]:
        """Get state value."""
        return await self.state_service.get_state(state_key, session_id)
