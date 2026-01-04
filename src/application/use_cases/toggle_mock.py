"""Use case for toggling mock enabled status."""

from src.domain.entities.mock_definition import MockDefinition
from src.domain.repositories.mock_repository import MockRepository
from src.application.exceptions import MockNotFoundError


class ToggleMockUseCase:
    """Toggle mock enabled/disabled status.

    Business rules:
    - Find existing mock (raise MockNotFoundError if missing)
    - Flip enabled flag (True → False, False → True)
    - Persist updated entity
    - Return updated mock
    """

    def __init__(self, repository: MockRepository):
        """Initialize use case with repository dependency.

        Args:
            repository: Mock repository for persistence
        """
        self.repository = repository

    async def execute(self, mock_id: str) -> MockDefinition:
        """Toggle mock enabled status.

        Args:
            mock_id: ID of mock to toggle

        Returns:
            Updated MockDefinition entity

        Raises:
            MockNotFoundError: If mock not found
        """
        existing = await self.repository.get_by_id(mock_id)
        if not existing:
            raise MockNotFoundError(f"Mock {mock_id} not found")

        existing.mock_enabled = not existing.mock_enabled
        updated = await self.repository.update(existing)
        return updated
