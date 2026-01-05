"""Authentication dependencies."""

from src.domain.services.jwt_service import JWTService
from src.domain.repositories.user_repository import (
    UserRepository,
    InMemoryUserRepository,
)
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.manage_api_keys import (
    GenerateAPIKeyUseCase,
    RevokeAPIKeyUseCase,
)


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


def get_register_user_use_case() -> RegisterUserUseCase:
    """Dependency: Get register user use case."""
    return RegisterUserUseCase(user_repository=_user_repository)


def get_generate_api_key_use_case() -> GenerateAPIKeyUseCase:
    """Dependency: Get generate API key use case."""
    return GenerateAPIKeyUseCase(user_repository=_user_repository)


def get_revoke_api_key_use_case() -> RevokeAPIKeyUseCase:
    """Dependency: Get revoke API key use case."""
    return RevokeAPIKeyUseCase(user_repository=_user_repository)
