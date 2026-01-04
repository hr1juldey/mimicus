"""User entity for authentication."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class User:
    """User entity with authentication and authorization.

    Attributes:
        user_id: Unique user identifier
        username: Username for login
        email: User email address
        password_hash: Hashed password (never plain text)
        roles: List of roles (admin, viewer, mock-user)
        api_key: Optional API key for programmatic access
        is_active: Whether user account is active
    """

    user_id: str
    username: str
    email: str
    password_hash: str
    roles: List[str] = field(default_factory=lambda: ["viewer"])
    api_key: Optional[str] = None
    is_active: bool = True

    def has_role(self, role: str) -> bool:
        """Check if user has specific role.

        Args:
            role: Role to check (admin, viewer, mock-user)

        Returns:
            True if user has role, False otherwise
        """
        return role in self.roles

    def has_any_role(self, roles: List[str]) -> bool:
        """Check if user has any of the given roles.

        Args:
            roles: List of roles to check

        Returns:
            True if user has any role, False otherwise
        """
        return any(role in self.roles for role in roles)
