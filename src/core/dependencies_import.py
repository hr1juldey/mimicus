"""Import feature dependencies."""

from src.domain.repositories.mock_repository import (
    MockRepository,
    InMemoryMockRepository,
)
from src.domain.services.mock_factory import MockFactory
from src.infrastructure.storage.file_storage import FileStorage, LocalFileStorage
from src.infrastructure.external.openapi_importer import OpenAPIImporter
from src.application.use_cases.import_openapi import ImportOpenAPIUseCase


# Singletons
_mock_repository: MockRepository = InMemoryMockRepository()
_mock_factory: MockFactory = MockFactory()
_file_storage: FileStorage = LocalFileStorage()
_openapi_importer: OpenAPIImporter = OpenAPIImporter(factory=_mock_factory)


def get_file_storage() -> FileStorage:
    """Dependency: Get file storage."""
    return _file_storage


def get_openapi_importer() -> OpenAPIImporter:
    """Dependency: Get OpenAPI importer."""
    return _openapi_importer


def get_import_openapi_use_case() -> ImportOpenAPIUseCase:
    """Dependency: Get import OpenAPI use case."""
    return ImportOpenAPIUseCase(
        repository=_mock_repository,
        importer=_openapi_importer,
        storage=_file_storage,
    )
