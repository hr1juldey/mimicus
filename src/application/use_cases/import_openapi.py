"""Use case for importing OpenAPI specifications."""

from typing import Dict, Any, List

from src.domain.entities.mock_definition import MockDefinition
from src.domain.repositories.mock_repository import MockRepository
from src.infrastructure.storage.file_storage import FileStorage
from src.infrastructure.external.openapi_importer import OpenAPIImporter
from src.application.exceptions import InvalidJSONError


class ImportOpenAPIUseCase:
    """Import OpenAPI spec and create mock definitions.

    Business rules:
    - Parse and validate OpenAPI specification
    - Generate mock for each endpoint
    - Save spec file for reference
    - Persist all generated mocks
    - Return import summary with created mocks
    """

    def __init__(
        self,
        repository: MockRepository,
        importer: OpenAPIImporter,
        storage: FileStorage,
    ):
        """Initialize use case with dependencies.

        Args:
            repository: Mock repository for persistence
            importer: OpenAPI importer for spec parsing
            storage: File storage for spec files
        """
        self.repository = repository
        self.importer = importer
        self.storage = storage

    async def execute(
        self, spec_content: str, filename: str, is_yaml: bool = False
    ) -> Dict[str, Any]:
        """Import OpenAPI spec and create mocks.

        Args:
            spec_content: OpenAPI specification content
            filename: Filename for storage
            is_yaml: True if YAML format

        Returns:
            Dict with spec_path, mocks_created, and mock list

        Raises:
            InvalidJSONError: If spec is invalid
        """
        try:
            mocks = await self.importer.import_spec(spec_content, is_yaml)
        except ValueError as e:
            raise InvalidJSONError(str(e))

        spec_path = await self.storage.save(
            f"openapi/{filename}", spec_content.encode()
        )

        created: List[MockDefinition] = []
        for mock in mocks:
            created_mock = await self.repository.create(mock)
            created.append(created_mock)

        return {
            "spec_path": spec_path,
            "mocks_created": len(created),
            "mocks": created,
        }
