"""Data Transfer Objects for authentication."""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    """DTO for login request."""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """DTO for token response."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")


class UserResponse(BaseModel):
    """DTO for user response."""

    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    roles: List[str] = Field(..., description="User roles")
    is_active: bool = Field(..., description="Is user active")


class APIKeyResponse(BaseModel):
    """DTO for API key response."""

    api_key: str = Field(..., description="Generated API key")
    user_id: str = Field(..., description="User ID")


class RefreshTokenRequest(BaseModel):
    """DTO for refresh token request."""

    refresh_token: str = Field(..., description="Refresh token")


class RegisterRequest(BaseModel):
    """DTO for user registration."""

    username: str = Field(..., min_length=3, description="Username")
    email: str = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password")


class RegisterResponse(BaseModel):
    """DTO for registration response."""

    user_id: str = Field(..., description="New user ID")
    username: str = Field(..., description="Username")
    api_key: str = Field(..., description="Generated API key")
