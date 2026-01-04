"""JWT encoding and decoding utilities."""

import json
import hmac
import hashlib
import base64
from typing import Dict, Any


class JWTEncoder:
    """JWT encoding/decoding helper with HS256 algorithm."""

    def __init__(self, secret: str):
        """Initialize encoder with secret key.

        Args:
            secret: Secret key for signing
        """
        self.secret = secret

    def encode(self, payload: Dict[str, Any]) -> str:
        """Encode payload to JWT token."""
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = self._base64_url_encode(json.dumps(header))
        payload_b64 = self._base64_url_encode(json.dumps(payload))

        msg = f"{header_b64}.{payload_b64}"
        signature = hmac.new(
            self.secret.encode(),
            msg.encode(),
            hashlib.sha256,
        ).digest()
        signature_b64 = self._base64_url_encode(signature)

        return f"{msg}.{signature_b64}"

    def decode(self, token: str) -> Dict[str, Any]:
        """Decode JWT token."""
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        payload_b64 = parts[1]
        payload_json = self._base64_url_decode(payload_b64)
        return json.loads(payload_json)

    def _base64_url_encode(self, data: str | bytes) -> str:
        """Base64 URL encode."""
        if isinstance(data, str):
            data = data.encode()
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    def _base64_url_decode(self, data: str) -> str:
        """Base64 URL decode."""
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data).decode()
