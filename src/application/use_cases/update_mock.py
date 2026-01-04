"""Use case for updating mock definitions."""

from src.domain.entities.mock_definition import MockDefinition
from src.application.dtos.mock_dtos import UpdateMockDTO
from src.application.mappers.mock_mapper import MockMapper
from src.domain.repositories.mock_repository import MockRepository
from src.application.exceptions import MockNotFoundError


class UpdateMockUseCase:
    """Update an existing mock definition.

    Business rules:
    - Verify mock exists (raise MockNotFoundError if missing)
    - Apply partial updates (only non-None fields)
    - Persist updated entity
    - Return updated mock
    """

    def __init__(self, repository: MockRepository, mapper: MockMapper):
        """Initialize use case with dependencies.

        Args:
            repository: Mock repository for persistence
            mapper: Mapper for applying updates
        """
        self.repository = repository
        self.mapper = mapper

    async def execute(
        self, mock_id: str, dto: UpdateMockDTO
    ) -> MockDefinition:
        """Update existing mock definition.

        Args:
            mock_id: ID of mock to update
            dto: Update mock data transfer object

        Returns:
            Updated MockDefinition entity

        Raises:
            MockNotFoundError: If mock not found
        """
        existing = await self.repository.get_by_id(mock_id)
        if not existing:
            raise MockNotFoundError(f"Mock {mock_id} not found")

        updated = self.mapper.apply_update(existing, dto)
        saved = await self.repository.update(updated)
        return saved
