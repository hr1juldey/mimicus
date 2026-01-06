"""Unit tests for user authentication use case."""

import pytest
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.auth_exceptions import InvalidCredentialsError
from src.domain.repositories.user_repository import InMemoryUserRepository
from src.domain.services.jwt_service import JWTService


@pytest.fixture
def user_repository():
    """Fixture providing user repository."""
    return InMemoryUserRepository()


@pytest.fixture
def jwt_service():
    """Fixture providing JWT service."""
    return JWTService()


@pytest.fixture
def use_case(user_repository, jwt_service):
    """Fixture providing authenticate use case."""
    return AuthenticateUserUseCase(user_repository, jwt_service)


class TestAuthenticateUserUseCase:
    """Test user authentication."""

    @pytest.mark.asyncio
    async def test_login_with_correct_credentials(self, use_case):
        """Test login with correct admin credentials."""
        # Default admin is created with password "admin123"
        result = await use_case.execute("admin", "admin123")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["expires_in"] == 3600

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(self, use_case):
        """Test login with wrong password."""
        with pytest.raises(InvalidCredentialsError):
            await use_case.execute("admin", "wrong_password")

    @pytest.mark.asyncio
    async def test_login_with_nonexistent_user(self, use_case):
        """Test login with nonexistent username."""
        with pytest.raises(InvalidCredentialsError):
            await use_case.execute("nonexistent", "password123")

    @pytest.mark.asyncio
    async def test_login_with_empty_username(self, use_case):
        """Test login with empty username."""
        with pytest.raises(InvalidCredentialsError):
            await use_case.execute("", "password")

    @pytest.mark.asyncio
    async def test_login_with_empty_password(self, use_case):
        """Test login with empty password."""
        with pytest.raises(InvalidCredentialsError):
            await use_case.execute("admin", "")

    @pytest.mark.asyncio
    async def test_returned_tokens_are_valid(self, use_case, jwt_service):
        """Test that returned tokens can be verified."""
        result = await use_case.execute("admin", "admin123")
        access_token = result["access_token"]

        payload = jwt_service.verify_token(access_token)
        assert payload is not None
        assert payload["username"] == "admin"
        assert "admin" in payload["roles"]
        assert payload["type"] == "access"

    @pytest.mark.asyncio
    async def test_refresh_token_validity(self, use_case, jwt_service):
        """Test that refresh token can be verified."""
        result = await use_case.execute("admin", "admin123")
        refresh_token = result["refresh_token"]

        payload = jwt_service.verify_token(refresh_token)
        assert payload is not None
        assert payload["type"] == "refresh"
