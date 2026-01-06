"""State entity for session/client-scoped key-value storage."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class State:
    """Represents a state key-value pair scoped by session or client."""

    state_key: str
    state_value: str
    session_id: Optional[str] = None
    mock_id: Optional[str] = None
    client_ip: Optional[str] = None
    state_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert state to dictionary."""
        return {
            "state_id": self.state_id,
            "state_key": self.state_key,
            "state_value": self.state_value,
            "session_id": self.session_id,
            "mock_id": self.mock_id,
            "client_ip": self.client_ip,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(
        state_key: str,
        state_value: str,
        session_id: Optional[str] = None,
        mock_id: Optional[str] = None,
        client_ip: Optional[str] = None,
    ) -> "State":
        """Create new state entity."""
        return State(
            state_key=state_key,
            state_value=state_value,
            session_id=session_id,
            mock_id=mock_id,
            client_ip=client_ip,
        )
