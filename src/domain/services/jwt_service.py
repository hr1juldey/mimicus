"""JWT token handling service."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from src.core.config import get_settings
from src.domain.services.jwt_encoder import JWTEncoder


class JWTService:
    """JWT token creation and validation service."""

    def __init__(self):
        """Initialize JWT service with config."""
        settings = get_settings()
        self.encoder = JWTEncoder(settings.config_jwt_secret)

    def create_access_token(
        self, user_id: str, username: str, roles: list, expires_in: int = 3600
    ) -> str:
        """Create JWT access token."""
        now = datetime.now(timezone.utc)
        exp = now + timedelta(seconds=expires_in)

        payload = {
            "user_id": user_id,
            "username": username,
            "roles": roles,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "type": "access",
        }

        return self.encoder.encode(payload)

    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token."""
        now = datetime.now(timezone.utc)
        exp = now + timedelta(days=7)

        payload = {
            "user_id": user_id,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "type": "refresh",
        }

        return self.encoder.encode(payload)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode token.

        Args:
            token: JWT token to verify

        Returns:
            Decoded payload if valid, None if invalid/expired
        """
        try:
            payload = self.encoder.decode(token)
            now = datetime.now(timezone.utc)
            if payload.get("exp", 0) < now.timestamp():
                return None
            return payload
        except Exception:
            return None
