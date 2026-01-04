"""Use case for deleting mock definitions."""

from src.domain.repositories.mock_repository import MockRepository
from src.application.exceptions import MockNotFoundError


class DeleteMockUseCase:
    """Delete an existing mock definition.

    Business rules:
    - Verify mock exists (raise MockNotFoundError if missing)
    - Delete from repository
    - Return success (None)
    """

    def __init__(self, repository: MockRepository):
        """Initialize use case with repository dependency.

        Args:
            repository: Mock repository for persistence
        """
        self.repository = repository

    async def execute(self, mock_id: str) -> None:
        """Delete mock definition by ID.

        Args:
            mock_id: ID of mock to delete

        Raises:
            MockNotFoundError: If mock not found
        """
        existing = await self.repository.get_by_id(mock_id)
        if not existing:
            raise MockNotFoundError(f"Mock {mock_id} not found")

        await self.repository.delete(mock_id)
