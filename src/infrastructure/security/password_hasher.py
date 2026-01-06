"""Password hashing using bcrypt for secure storage."""

import hashlib
import os


class PasswordHasher:
    """Simple password hashing without external dependencies."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using PBKDF2 with SHA256.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password string with salt prefix
        """
        salt = os.urandom(32)
        # Use PBKDF2 with 100,000 iterations
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        # Return salt + hash as hex string
        return f"pbkdf2$100000${salt.hex()}${hashed.hex()}"

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        try:
            parts = hashed_password.split("$")
            if len(parts) != 4 or parts[0] != "pbkdf2":
                return False

            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            stored_hash = bytes.fromhex(parts[3])

            computed_hash = hashlib.pbkdf2_hmac(
                "sha256", plain_password.encode(), salt, iterations
            )
            return computed_hash == stored_hash
        except Exception:
            return False

    @staticmethod
    def get_default_admin_hash() -> str:
        """Get hash for default admin password 'admin123'.

        Returns:
            Pre-computed hash for testing/default setup
        """
        # Pre-computed hash for "admin123"
        return PasswordHasher.hash_password("admin123")
