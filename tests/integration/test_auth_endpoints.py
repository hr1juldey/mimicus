"""Integration tests for authentication endpoints."""

import pytest
import json
from fastapi.testclient import TestClient
from src.core.app import create_app


app = create_app()
client = TestClient(app)


class TestAuthLogin:
    """Test login endpoint."""

    def test_login_with_default_admin_credentials(self):
        """Test login with default admin user."""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600

    def test_login_with_wrong_password(self):
        """Test login with wrong password."""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrong_password"},
        )

        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]

    def test_login_with_nonexistent_user(self):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401

    def test_login_response_has_valid_token(self):
        """Test that login response contains valid JWT token."""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"},
        )

        data = response.json()
        access_token = data["access_token"]

        # Verify token structure
        parts = access_token.split(".")
        assert len(parts) == 3  # JWT has 3 parts


class TestAuthRegister:
    """Test registration endpoint."""

    def test_register_new_user(self):
        """Test registering a new user."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "secure_password_123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert "user_id" in data
        assert "api_key" in data

    def test_register_duplicate_username(self):
        """Test registering with duplicate username."""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "username": "duplicate",
                "email": "first@example.com",
                "password": "password123",
            },
        )

        # Second registration with same username
        response = client.post(
            "/api/auth/register",
            json={
                "username": "duplicate",
                "email": "second@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "already taken" in response.json()["detail"].lower()

    def test_register_cannot_use_admin_username(self):
        """Test cannot register with admin username."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "admin",
                "email": "fake@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 400

    def test_register_short_username(self):
        """Test registering with username too short."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "ab",
                "email": "user@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_register_short_password(self):
        """Test registering with password too short."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "user@example.com",
                "password": "short",
            },
        )

        assert response.status_code == 422  # Validation error


class TestAuthRefresh:
    """Test token refresh endpoint."""

    def test_refresh_token(self):
        """Test refreshing access token."""
        # Get tokens
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["refresh_token"] == refresh_token

    def test_refresh_with_access_token_fails(self):
        """Test that refresh with access token fails."""
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        access_token = login_response.json()["access_token"]

        # Try to refresh with access token
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": access_token},
        )

        assert response.status_code == 401

    def test_refresh_with_invalid_token(self):
        """Test refresh with invalid token."""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid.token.here"},
        )

        assert response.status_code == 401


class TestAuthIntegration:
    """Integration tests for auth flow."""

    def test_full_auth_flow(self):
        """Test complete authentication flow."""
        # 1. Register new user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "flowuser",
                "email": "flow@example.com",
                "password": "flow_password_123",
            },
        )
        assert register_response.status_code == 200

        # 2. Login with new user
        login_response = client.post(
            "/api/auth/login",
            json={"username": "flowuser", "password": "flow_password_123"},
        )
        assert login_response.status_code == 200
        data = login_response.json()
        access_token = data["access_token"]

        # 3. Use access token in header
        headers = {"Authorization": f"Bearer {access_token}"}
        # This would be used to access protected endpoints

        # 4. Refresh token
        refresh_response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": data["refresh_token"]},
        )
        assert refresh_response.status_code == 200
