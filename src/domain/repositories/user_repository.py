"""Repository for user persistence."""

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User


class UserRepository(ABC):
    """Abstract user repository interface."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        """Delete user."""
        pass


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of user repository."""

    def __init__(self):
        """Initialize with default admin user."""
        self._users: dict[str, User] = {}
        # Create default admin user for testing
        admin = User(
            user_id="admin-001",
            username="admin",
            email="admin@mimicus.local",
            password_hash="$2b$12$hash",
            roles=["admin", "viewer"],
        )
        self._users[admin.user_id] = admin

    async def create(self, user: User) -> User:
        """Create and persist user."""
        self._users[user.user_id] = user
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    async def update(self, user: User) -> User:
        """Update user."""
        self._users[user.user_id] = user
        return user

    async def delete(self, user_id: str) -> None:
        """Delete user."""
        self._users.pop(user_id, None)
