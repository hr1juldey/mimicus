"""Use case for user authentication."""

from src.domain.repositories.user_repository import UserRepository
from src.domain.services.jwt_service import JWTService
from src.application.auth_exceptions import InvalidCredentialsError
from src.infrastructure.security import PasswordHasher


class AuthenticateUserUseCase:
    """Authenticate user with credentials.

    Business rules:
    - Verify user exists by username
    - Verify password matches hash using PBKDF2
    - Generate JWT tokens on success
    - Raise InvalidCredentialsError on failure
    """

    def __init__(self, user_repository: UserRepository, jwt_service: JWTService):
        """Initialize use case with dependencies.

        Args:
            user_repository: User repository for lookups
            jwt_service: JWT service for token generation
        """
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, username: str, password: str) -> dict[str, str | int]:
        """Authenticate user and generate tokens.

        Args:
            username: Username to authenticate
            password: Password to verify

        Returns:
            Dict with access_token, refresh_token, and expires_in

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        user = await self.user_repository.get_by_username(username)
        if not user or not user.is_active:
            raise InvalidCredentialsError("Invalid username or password")

        if not PasswordHasher.verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")

        access_token = self.jwt_service.create_access_token(
            user.user_id, user.username, user.roles
        )
        refresh_token = self.jwt_service.create_refresh_token(user.user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600,
        }
