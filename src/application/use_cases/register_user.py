"""Use case for user registration."""

import uuid
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.application.auth_exceptions import AuthError
from src.infrastructure.security import PasswordHasher


class UserAlreadyExistsError(AuthError):
    """Raised when user with username already exists."""

    pass


class RegisterUserUseCase:
    """Register a new user account.

    Business rules:
    - Username must be unique
    - Password must be hashed with PBKDF2
    - New users get 'viewer' role by default
    - Generate API key for programmatic access
    """

    def __init__(self, user_repository: UserRepository):
        """Initialize use case with dependencies.

        Args:
            user_repository: User repository for persistence
        """
        self.user_repository = user_repository

    async def execute(
        self, username: str, email: str, password: str
    ) -> dict[str, str]:
        """Register new user.

        Args:
            username: Desired username (must be unique)
            email: User email address
            password: Plain text password to hash

        Returns:
            Dict with user_id and api_key

        Raises:
            UserAlreadyExistsError: If username exists
        """
        # Check if user already exists
        existing = await self.user_repository.get_by_username(username)
        if existing:
            raise UserAlreadyExistsError(f"Username '{username}' already taken")

        # Create new user
        user_id = str(uuid.uuid4())
        password_hash = PasswordHasher.hash_password(password)
        api_key = str(uuid.uuid4())

        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            roles=["viewer"],
            api_key=api_key,
            is_active=True,
        )

        await self.user_repository.create(user)

        return {"user_id": user_id, "api_key": api_key}
