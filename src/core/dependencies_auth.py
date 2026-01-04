"""Authentication dependencies."""

from src.domain.services.jwt_service import JWTService
from src.domain.repositories.user_repository import (
    UserRepository,
    InMemoryUserRepository,
)
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase


# Singletons
_user_repository: UserRepository = InMemoryUserRepository()
_jwt_service: JWTService = JWTService()


def get_jwt_service() -> JWTService:
    """Dependency: Get JWT service."""
    return _jwt_service


def get_user_repository() -> UserRepository:
    """Dependency: Get user repository."""
    return _user_repository


def get_authenticate_user_use_case() -> AuthenticateUserUseCase:
    """Dependency: Get authenticate user use case."""
    return AuthenticateUserUseCase(
        user_repository=_user_repository, jwt_service=_jwt_service
    )
