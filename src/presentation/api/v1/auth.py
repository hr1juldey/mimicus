"""Authentication endpoints for login and token management."""

from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import get_authenticate_user_use_case, get_jwt_service
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.services.jwt_service import JWTService
from src.application.dtos.auth_dtos import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from src.application.auth_exceptions import InvalidCredentialsError


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
) -> TokenResponse:
    """Login with username and password.

    Args:
        request: Login credentials

    Returns:
        TokenResponse with access and refresh tokens

    Raises:
        HTTPException: If credentials invalid
    """
    try:
        result = await use_case.execute(request.username, request.password)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            expires_in=result["expires_in"],
        )
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    jwt_service: JWTService = Depends(get_jwt_service),
) -> TokenResponse:
    """Refresh expired access token.

    Args:
        request: Refresh token request

    Returns:
        TokenResponse with new access token

    Raises:
        HTTPException: If refresh token invalid
    """
    payload = jwt_service.verify_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("user_id")
    access_token = jwt_service.create_access_token(
        user_id=user_id, username="", roles=[]
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token,
        expires_in=3600,
    )
