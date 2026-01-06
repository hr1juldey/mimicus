"""Service for managing state operations."""

from typing import Optional
from src.domain.entities.state import State
from src.domain.repositories.state_repository import StateRepository


class StateService:
    """Encapsulates state business logic."""

    def __init__(self, repository: StateRepository):
        """Initialize with state repository."""
        self.repository = repository

    async def get_state(
        self, state_key: str, session_id: Optional[str] = None
    ) -> Optional[str]:
        """Get state value by key."""
        state = await self.repository.get(state_key, session_id)
        return state.state_value if state else None

    async def set_state(
        self, state_key: str, state_value: str, session_id: Optional[str] = None
    ) -> None:
        """Set state value."""
        state = State.create(
            state_key=state_key,
            state_value=state_value,
            session_id=session_id,
        )
        await self.repository.set(state)

    async def increment_counter(
        self, state_key: str, session_id: Optional[str] = None, delta: int = 1
    ) -> int:
        """Atomically increment counter, return new value."""
        return await self.repository.increment(state_key, session_id, delta)

    async def delete_state(
        self, state_key: str, session_id: Optional[str] = None
    ) -> bool:
        """Delete state by key."""
        return await self.repository.delete(state_key, session_id)

    async def get_session_state(self, session_id: str) -> dict:
        """Get all state for a session as dict."""
        states = await self.repository.get_by_session(session_id)
        return {s.state_key: s.state_value for s in states}

    async def clear_session_state(self, session_id: str) -> int:
        """Clear all state for session, return count deleted."""
        return await self.repository.clear_session(session_id)
