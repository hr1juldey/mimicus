"""Use case for listing mock definitions."""

from typing import List, Optional

from src.domain.entities.mock_definition import MockDefinition
from src.domain.repositories.mock_repository import MockRepository


class ListMocksUseCase:
    """List mock definitions with optional filtering.

    Business rules:
    - Return all mocks or filtered subset
    - Support filtering by enabled status
    - Support filtering by minimum priority
    - Sort by priority (descending)
    """

    def __init__(self, repository: MockRepository):
        """Initialize use case with repository dependency.

        Args:
            repository: Mock repository for data access
        """
        self.repository = repository

    async def execute(
        self,
        enabled_only: bool = False,
        min_priority: Optional[int] = None,
    ) -> List[MockDefinition]:
        """List all mocks with optional filters.

        Args:
            enabled_only: If True, only return enabled mocks
            min_priority: If set, only return mocks with priority >= value

        Returns:
            List of MockDefinition entities sorted by priority (descending)
        """
        all_mocks = await self.repository.get_all()

        if enabled_only:
            all_mocks = [m for m in all_mocks if m.mock_enabled]

        if min_priority is not None:
            all_mocks = [m for m in all_mocks if m.mock_priority >= min_priority]

        return sorted(all_mocks, key=lambda m: m.mock_priority, reverse=True)
