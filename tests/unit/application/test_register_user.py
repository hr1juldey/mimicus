"""Unit tests for user registration use case."""

import pytest
from src.application.use_cases.register_user import (
    RegisterUserUseCase,
    UserAlreadyExistsError,
)
from src.domain.repositories.user_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    """Fixture providing user repository."""
    return InMemoryUserRepository()


@pytest.fixture
def use_case(user_repository):
    """Fixture providing register use case."""
    return RegisterUserUseCase(user_repository)


class TestRegisterUserUseCase:
    """Test user registration."""

    @pytest.mark.asyncio
    async def test_register_new_user(self, use_case):
        """Test registering a new user."""
        result = await use_case.execute("newuser", "user@example.com", "secure_pass")

        assert "user_id" in result
        assert "api_key" in result
        assert result["user_id"] != ""
        assert result["api_key"] != ""

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, use_case):
        """Test registering with duplicate username."""
        await use_case.execute("duplicate", "user1@example.com", "password123")

        with pytest.raises(UserAlreadyExistsError):
            await use_case.execute("duplicate", "user2@example.com", "password123")

    @pytest.mark.asyncio
    async def test_register_cannot_use_admin_username(self, use_case):
        """Test that cannot register with existing admin username."""
        with pytest.raises(UserAlreadyExistsError):
            await use_case.execute("admin", "user@example.com", "password123")

    @pytest.mark.asyncio
    async def test_registered_user_has_viewer_role(self, user_repository, use_case):
        """Test that registered user gets viewer role."""
        result = await use_case.execute("newuser", "user@example.com", "pass123")
        user = await user_repository.get_by_id(result["user_id"])

        assert "viewer" in user.roles
        assert "admin" not in user.roles

    @pytest.mark.asyncio
    async def test_registered_user_is_active(self, user_repository, use_case):
        """Test that registered user is active by default."""
        result = await use_case.execute("newuser", "user@example.com", "pass123")
        user = await user_repository.get_by_id(result["user_id"])

        assert user.is_active is True

    @pytest.mark.asyncio
    async def test_registered_user_has_api_key(self, user_repository, use_case):
        """Test that registered user gets API key."""
        result = await use_case.execute("newuser", "user@example.com", "pass123")
        user = await user_repository.get_by_id(result["user_id"])

        assert user.api_key is not None
        assert user.api_key == result["api_key"]

    @pytest.mark.asyncio
    async def test_registered_user_can_login(self, use_case, user_repository):
        """Test that registered user can successfully login."""
        # Register user
        register_result = await use_case.execute(
            "logintest", "user@example.com", "mypassword"
        )

        # Try to login
        from src.domain.services.jwt_service import JWTService
        from src.application.use_cases.authenticate_user import AuthenticateUserUseCase

        jwt_service = JWTService()
        auth_use_case = AuthenticateUserUseCase(user_repository, jwt_service)
        login_result = await auth_use_case.execute("logintest", "mypassword")

        assert "access_token" in login_result

    @pytest.mark.asyncio
    async def test_multiple_registrations_generate_different_ids(self, use_case):
        """Test that multiple registrations generate different user IDs."""
        result1 = await use_case.execute("user1", "user1@example.com", "pass123")
        result2 = await use_case.execute("user2", "user2@example.com", "pass123")

        assert result1["user_id"] != result2["user_id"]
        assert result1["api_key"] != result2["api_key"]
