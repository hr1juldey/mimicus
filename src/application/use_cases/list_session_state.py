"""Use case for listing session state."""

from src.domain.services.state_service import StateService


class ListSessionStateUseCase:
    """List all state for a session."""

    def __init__(self, state_service: StateService):
        """Initialize use case."""
        self.state_service = state_service

    async def execute(self, session_id: str) -> dict:
        """Get all state for session."""
        return await self.state_service.get_session_state(session_id)
