"""Dependency injection functions for FastAPI routes."""

from src.core.config import get_settings, Settings
from src.domain.repositories.mock_repository import (
    MockRepository,
    InMemoryMockRepository,
)
from src.domain.services.matching_service import MatchingService
from src.domain.services.response_service import ResponseService
from src.domain.services.template_service import TemplateService
from src.domain.services.mock_factory import MockFactory
from src.domain.services.rate_limiter_service import RateLimiterService
from src.application.mappers.mock_mapper import MockMapper
from src.application.use_cases import (
    CreateMockUseCase,
    UpdateMockUseCase,
    DeleteMockUseCase,
    ListMocksUseCase,
    GetMockUseCase,
    ToggleMockUseCase,
    BulkImportUseCase,
)
from src.infrastructure.database.connection import get_database
from src.core.dependencies_auth import (
    get_jwt_service,
    get_user_repository,
    get_authenticate_user_use_case,
    get_register_user_use_case,
    get_generate_api_key_use_case,
    get_revoke_api_key_use_case,
)
from src.core.dependencies_import import (
    get_file_storage,
    get_openapi_importer,
    get_import_openapi_use_case,
)
from src.domain.repositories.state_repository import (
    StateRepository,
    InMemoryStateRepository,
)
from src.domain.services.state_service import StateService

__all__ = [
    "get_settings_dep",
    "get_mock_repository",
    "get_matching_service",
    "get_response_service",
    "get_template_service",
    "get_database_dep",
    "get_mock_mapper",
    "get_rate_limiter",
    "get_create_mock_use_case",
    "get_update_mock_use_case",
    "get_delete_mock_use_case",
    "get_list_mocks_use_case",
    "get_get_mock_use_case",
    "get_toggle_mock_use_case",
    "get_bulk_import_use_case",
    "get_jwt_service",
    "get_user_repository",
    "get_authenticate_user_use_case",
    "get_register_user_use_case",
    "get_generate_api_key_use_case",
    "get_revoke_api_key_use_case",
    "get_file_storage",
    "get_openapi_importer",
    "get_import_openapi_use_case",
    "get_state_repository",
    "get_state_service",
]


# Global singleton instances
_mock_repository: MockRepository = InMemoryMockRepository()
_state_repository: StateRepository = InMemoryStateRepository()
_matching_service: MatchingService = MatchingService()
_rate_limiter: RateLimiterService = RateLimiterService()
_state_service: StateService = StateService(repository=_state_repository)
_template_service: TemplateService = TemplateService(state_service=_state_service)
_response_service: ResponseService = ResponseService(
    template_service=_template_service, rate_limiter=_rate_limiter
)
_mock_mapper: MockMapper = MockMapper()
_mock_factory: MockFactory = MockFactory()


def get_settings_dep() -> Settings:
    """Dependency: Get application settings."""
    return get_settings()


def get_mock_repository() -> MockRepository:
    """Dependency: Get mock repository instance."""
    return _mock_repository


def get_matching_service() -> MatchingService:
    """Dependency: Get matching service instance."""
    return _matching_service


def get_response_service() -> ResponseService:
    """Dependency: Get response service instance."""
    return _response_service


def get_template_service() -> TemplateService:
    """Dependency: Get template service instance."""
    return _template_service


def get_database_dep():
    """Dependency: Get database connection."""
    return get_database()


def get_mock_mapper() -> MockMapper:
    """Dependency: Get mock mapper instance."""
    return _mock_mapper


def get_rate_limiter() -> RateLimiterService:
    """Dependency: Get rate limiter instance."""
    return _rate_limiter


def get_create_mock_use_case() -> CreateMockUseCase:
    """Dependency: Get create mock use case."""
    return CreateMockUseCase(repository=_mock_repository, mapper=_mock_mapper)


def get_update_mock_use_case() -> UpdateMockUseCase:
    """Dependency: Get update mock use case."""
    return UpdateMockUseCase(repository=_mock_repository, mapper=_mock_mapper)


def get_delete_mock_use_case() -> DeleteMockUseCase:
    """Dependency: Get delete mock use case."""
    return DeleteMockUseCase(repository=_mock_repository)


def get_list_mocks_use_case() -> ListMocksUseCase:
    """Dependency: Get list mocks use case."""
    return ListMocksUseCase(repository=_mock_repository)


def get_get_mock_use_case() -> GetMockUseCase:
    """Dependency: Get get mock use case."""
    return GetMockUseCase(repository=_mock_repository)


def get_toggle_mock_use_case() -> ToggleMockUseCase:
    """Dependency: Get toggle mock use case."""
    return ToggleMockUseCase(repository=_mock_repository)


def get_bulk_import_use_case() -> BulkImportUseCase:
    """Dependency: Get bulk import use case."""
    return BulkImportUseCase(
        repository=_mock_repository, factory=_mock_factory, mapper=_mock_mapper
    )


def get_state_repository() -> StateRepository:
    """Dependency: Get state repository instance."""
    return _state_repository


def get_state_service() -> StateService:
    """Dependency: Get state service instance."""
    return _state_service
