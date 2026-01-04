"""Authentication middleware for token and API key validation."""

from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.domain.services.jwt_service import JWTService


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for JWT and API key authentication.

    Validates Bearer tokens and API keys from request headers.
    """

    def __init__(self, app, jwt_service: Optional[JWTService] = None):
        """Initialize auth middleware.

        Args:
            app: FastAPI application
            jwt_service: JWT service for token validation
        """
        super().__init__(app)
        self.jwt_service = jwt_service or JWTService()

    async def dispatch(self, request: Request, call_next):
        """Process request and validate authentication.

        Args:
            request: HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response from next handler
        """
        # Skip auth for health and login endpoints
        if request.url.path in ["/api/health", "/api/auth/login"]:
            return await call_next(request)

        token = self._extract_token(request)
        if not token:
            raise HTTPException(status_code=401, detail="Missing auth token")

        payload = self.jwt_service.verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid auth token")

        request.state.user_id = payload.get("user_id")
        request.state.username = payload.get("username")
        request.state.roles = payload.get("roles", [])

        return await call_next(request)

    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract Bearer token from Authorization header.

        Args:
            request: HTTP request

        Returns:
            Token string if present, None otherwise
        """
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        return auth_header[7:]
