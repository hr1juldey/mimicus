"""Dependency injection functions for FastAPI routes."""

from fastapi import Depends
from src.core.config import get_settings, Settings
from src.domain.repositories.mock_repository import MockRepository, InMemoryMockRepository
from src.domain.services.matching_service import MatchingService
from src.domain.services.response_service import ResponseService
from src.domain.services.template_service import TemplateService
from src.infrastructure.database.connection import get_database


# Global singleton instances
_mock_repository: MockRepository = InMemoryMockRepository()
_matching_service: MatchingService = MatchingService()
_template_service: TemplateService = TemplateService()
_response_service: ResponseService = ResponseService(template_service=_template_service)


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
