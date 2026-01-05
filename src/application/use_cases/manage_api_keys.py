"""Use case for API key management."""

import uuid
from src.domain.repositories.user_repository import UserRepository
from src.application.auth_exceptions import UnauthorizedError


class GenerateAPIKeyUseCase:
    """Generate a new API key for user.

    Business rules:
    - User can generate new API keys anytime
    - Old API key is replaced
    - API key is returned only once at creation
    """

    def __init__(self, user_repository: UserRepository):
        """Initialize use case with dependencies.

        Args:
            user_repository: User repository for persistence
        """
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> str:
        """Generate new API key for user.

        Args:
            user_id: User ID to generate key for

        Returns:
            New API key string

        Raises:
            UnauthorizedError: If user not found
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedError(f"User {user_id} not found")

        # Generate new API key
        api_key = str(uuid.uuid4())
        user.api_key = api_key

        await self.user_repository.update(user)
        return api_key


class RevokeAPIKeyUseCase:
    """Revoke user's API key.

    Business rules:
    - Revoked key cannot be used for authentication
    - User must generate new key to use API
    """

    def __init__(self, user_repository: UserRepository):
        """Initialize use case with dependencies.

        Args:
            user_repository: User repository for persistence
        """
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> None:
        """Revoke API key for user.

        Args:
            user_id: User ID to revoke key for

        Raises:
            UnauthorizedError: If user not found
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedError(f"User {user_id} not found")

        user.api_key = None
        await self.user_repository.update(user)
