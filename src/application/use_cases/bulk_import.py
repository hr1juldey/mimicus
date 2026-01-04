"""Use case for bulk importing mock definitions."""

import json
from typing import Dict, Any

from src.domain.repositories.mock_repository import MockRepository
from src.domain.services.mock_factory import MockFactory
from src.application.dtos.mock_dtos import CreateMockDTO
from src.application.mappers.mock_mapper import MockMapper
from src.application.exceptions import InvalidJSONError


class BulkImportUseCase:
    """Import multiple mocks from JSON data.

    Business rules:
    - Parse JSON data
    - Validate each mock definition
    - Continue on errors (collect errors, don't fail batch)
    - Persist all valid mocks
    - Return summary with created count and error list
    """

    def __init__(
        self,
        repository: MockRepository,
        factory: MockFactory,
        mapper: MockMapper = None,
    ):
        """Initialize use case with dependencies.

        Args:
            repository: Mock repository for persistence
            factory: Factory for creating entities from dicts
            mapper: Optional mapper for DTO validation
        """
        self.repository = repository
        self.factory = factory
        self.mapper = mapper or MockMapper()

    async def execute(self, json_data: str) -> Dict[str, Any]:
        """Import multiple mocks from JSON.

        Args:
            json_data: JSON string with mocks array

        Returns:
            Dict with created count, error count, and error details

        Raises:
            InvalidJSONError: If JSON is malformed
        """
        try:
            data = json.loads(json_data)
            mocks_data = data.get("mocks", [])
        except json.JSONDecodeError as e:
            raise InvalidJSONError(f"Invalid JSON: {str(e)}")

        created = []
        errors = []

        for idx, mock_data in enumerate(mocks_data):
            try:
                dto = CreateMockDTO(**mock_data)
                mock = self.mapper.dto_to_entity(dto)
                created_mock = await self.repository.create(mock)
                created.append(created_mock)
            except Exception as e:
                errors.append(
                    {"index": idx, "error": str(e), "data": mock_data}
                )

        return {
            "created": len(created),
            "errors": len(errors),
            "mocks": created,
            "error_details": errors,
        }
