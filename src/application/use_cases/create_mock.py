"""Use case for creating mock definitions."""

from src.domain.entities.mock_definition import MockDefinition
from src.application.dtos.mock_dtos import CreateMockDTO
from src.application.mappers.mock_mapper import MockMapper
from src.domain.repositories.mock_repository import MockRepository


class CreateMockUseCase:
    """Create a new mock definition.

    Business rules:
    - Generate unique UUID for mock_id
    - Validate input via DTO
    - Persist to repository
    - Return created entity
    """

    def __init__(self, repository: MockRepository, mapper: MockMapper):
        """Initialize use case with dependencies.

        Args:
            repository: Mock repository for persistence
            mapper: Mapper for DTO to entity conversion
        """
        self.repository = repository
        self.mapper = mapper

    async def execute(self, dto: CreateMockDTO) -> MockDefinition:
        """Create and persist a new mock definition.

        Args:
            dto: Create mock data transfer object

        Returns:
            Created MockDefinition entity

        Raises:
            ValueError: If validation fails
        """
        entity = self.mapper.dto_to_entity(dto)
        created = await self.repository.create(entity)
        return created
