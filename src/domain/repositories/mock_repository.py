"""Mock repository interface and in-memory implementation."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.domain.entities.mock_definition import MockDefinition


class MockRepository(ABC):
    """Abstract repository interface for mock definitions."""

    @abstractmethod
    async def get_all(self) -> List[MockDefinition]:
        """Get all mock definitions."""
        pass

    @abstractmethod
    async def get_by_id(self, mock_id: str) -> Optional[MockDefinition]:
        """Get mock definition by ID."""
        pass

    @abstractmethod
    async def create(self, mock: MockDefinition) -> MockDefinition:
        """Create new mock definition."""
        pass

    @abstractmethod
    async def update(self, mock: MockDefinition) -> MockDefinition:
        """Update existing mock definition."""
        pass

    @abstractmethod
    async def delete(self, mock_id: str) -> bool:
        """Delete mock definition by ID."""
        pass


class InMemoryMockRepository(MockRepository):
    """In-memory implementation of MockRepository."""

    def __init__(self):
        """Initialize in-memory mock storage."""
        self._mocks: Dict[str, MockDefinition] = {}

    async def get_all(self) -> List[MockDefinition]:
        """Get all mock definitions sorted by priority descending."""
        mocks = list(self._mocks.values())
        return sorted(mocks, key=lambda m: m.mock_priority, reverse=True)

    async def get_by_id(self, mock_id: str) -> Optional[MockDefinition]:
        """Get mock definition by ID."""
        return self._mocks.get(mock_id)

    async def create(self, mock: MockDefinition) -> MockDefinition:
        """Create new mock definition."""
        self._mocks[mock.mock_id] = mock
        return mock

    async def update(self, mock: MockDefinition) -> MockDefinition:
        """Update existing mock definition."""
        if mock.mock_id not in self._mocks:
            raise ValueError(f"Mock {mock.mock_id} not found")
        self._mocks[mock.mock_id] = mock
        return mock

    async def delete(self, mock_id: str) -> bool:
        """Delete mock definition by ID."""
        if mock_id in self._mocks:
            del self._mocks[mock_id]
            return True
        return False
