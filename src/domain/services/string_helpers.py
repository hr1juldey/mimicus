"""String manipulation helpers."""

import hashlib
import base64


class StringHelpers:
    """String manipulation helpers."""

    def uppercase(self, text: str) -> str:
        """Convert text to uppercase."""
        return text.upper()

    def lowercase(self, text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()

    def md5(self, text: str) -> str:
        """Generate MD5 hash of text."""
        return hashlib.md5(text.encode()).hexdigest()

    def sha256(self, text: str) -> str:
        """Generate SHA-256 hash of text."""
        return hashlib.sha256(text.encode()).hexdigest()

    def base64_encode(self, text: str) -> str:
        """Base64 encode text."""
        return base64.b64encode(text.encode()).decode()

    def base64_decode(self, encoded_text: str) -> str:
        """Base64 decode text."""
        return base64.b64decode(encoded_text.encode()).decode()
