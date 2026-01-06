"""Use case for setting state."""

from typing import Optional
from src.domain.services.state_service import StateService


class SetStateUseCase:
    """Set state by key and session."""

    def __init__(self, state_service: StateService):
        """Initialize use case."""
        self.state_service = state_service

    async def execute(
        self, state_key: str, state_value: str, session_id: Optional[str] = None
    ) -> None:
        """Set state value."""
        await self.state_service.set_state(state_key, state_value, session_id)
