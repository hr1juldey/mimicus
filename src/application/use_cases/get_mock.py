"""Use case for retrieving a mock definition."""

from src.domain.entities.mock_definition import MockDefinition
from src.domain.repositories.mock_repository import MockRepository
from src.application.exceptions import MockNotFoundError


class GetMockUseCase:
    """Get a single mock definition by ID.

    Business rules:
    - Retrieve mock from repository
    - Raise MockNotFoundError if not found
    - Return entity
    """

    def __init__(self, repository: MockRepository):
        """Initialize use case with repository dependency.

        Args:
            repository: Mock repository for data access
        """
        self.repository = repository

    async def execute(self, mock_id: str) -> MockDefinition:
        """Get mock definition by ID.

        Args:
            mock_id: ID of mock to retrieve

        Returns:
            MockDefinition entity

        Raises:
            MockNotFoundError: If mock not found
        """
        mock = await self.repository.get_by_id(mock_id)
        if not mock:
            raise MockNotFoundError(f"Mock {mock_id} not found")
        return mock
