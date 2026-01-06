"""State repository interface and implementations."""

from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.state import State


class StateRepository(ABC):
    """Abstract repository for state persistence."""

    @abstractmethod
    async def get(
        self, state_key: str, session_id: Optional[str] = None
    ) -> Optional[State]:
        """Get state by key and optional session."""
        pass

    @abstractmethod
    async def set(self, state: State) -> State:
        """Persist state."""
        pass

    @abstractmethod
    async def increment(
        self, state_key: str, session_id: Optional[str] = None, delta: int = 1
    ) -> int:
        """Atomically increment counter, return new value."""
        pass

    @abstractmethod
    async def delete(
        self, state_key: str, session_id: Optional[str] = None
    ) -> bool:
        """Delete state, return True if deleted."""
        pass

    @abstractmethod
    async def get_by_session(self, session_id: str) -> List[State]:
        """Get all state for a session."""
        pass

    @abstractmethod
    async def clear_session(self, session_id: str) -> int:
        """Clear all state for session, return count deleted."""
        pass


class InMemoryStateRepository(StateRepository):
    """In-memory state repository for testing/development."""

    def __init__(self):
        """Initialize in-memory store."""
        self._store: dict[str, dict[str, str]] = {}

    async def get(
        self, state_key: str, session_id: Optional[str] = None
    ) -> Optional[State]:
        """Get state from memory."""
        session_id = session_id or "default"
        if session_id in self._store and state_key in self._store[session_id]:
            return State(
                state_key=state_key,
                state_value=self._store[session_id][state_key],
                session_id=session_id,
            )
        return None

    async def set(self, state: State) -> State:
        """Store state in memory."""
        session_id = state.session_id or "default"
        if session_id not in self._store:
            self._store[session_id] = {}
        self._store[session_id][state.state_key] = state.state_value
        return state

    async def increment(
        self, state_key: str, session_id: Optional[str] = None, delta: int = 1
    ) -> int:
        """Increment counter in memory."""
        session_id = session_id or "default"
        if session_id not in self._store:
            self._store[session_id] = {}
        current = int(self._store[session_id].get(state_key, 0))
        new_val = current + delta
        self._store[session_id][state_key] = str(new_val)
        return new_val

    async def delete(
        self, state_key: str, session_id: Optional[str] = None
    ) -> bool:
        """Delete from memory."""
        session_id = session_id or "default"
        if session_id in self._store and state_key in self._store[session_id]:
            del self._store[session_id][state_key]
            return True
        return False

    async def get_by_session(self, session_id: str) -> List[State]:
        """Get all state for session."""
        if session_id not in self._store:
            return []
        return [
            State(state_key=k, state_value=v, session_id=session_id)
            for k, v in self._store[session_id].items()
        ]

    async def clear_session(self, session_id: str) -> int:
        """Clear session from memory."""
        if session_id in self._store:
            count = len(self._store[session_id])
            del self._store[session_id]
            return count
        return 0
