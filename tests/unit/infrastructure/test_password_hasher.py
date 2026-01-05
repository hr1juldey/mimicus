"""Unit tests for password hasher."""

import pytest
from src.infrastructure.security import PasswordHasher


class TestPasswordHasher:
    """Test password hashing and verification."""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        hashed = PasswordHasher.hash_password("test_password")
        assert isinstance(hashed, str)
        assert "$" in hashed  # Should contain salt separators

    def test_hash_password_different_each_time(self):
        """Test that same password produces different hashes."""
        password = "test_password"
        hash1 = PasswordHasher.hash_password(password)
        hash2 = PasswordHasher.hash_password(password)
        assert hash1 != hash2  # Different salts produce different hashes

    def test_verify_password_correct(self):
        """Test verification with correct password."""
        password = "my_secure_password"
        hashed = PasswordHasher.hash_password(password)
        assert PasswordHasher.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verification with incorrect password."""
        password = "my_secure_password"
        hashed = PasswordHasher.hash_password(password)
        assert PasswordHasher.verify_password("wrong_password", hashed) is False

    def test_verify_password_empty_password(self):
        """Test verification with empty password."""
        hashed = PasswordHasher.hash_password("test")
        assert PasswordHasher.verify_password("", hashed) is False

    def test_verify_password_invalid_hash_format(self):
        """Test verification with invalid hash format."""
        assert PasswordHasher.verify_password("password", "invalid_hash") is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "MyPassword"
        hashed = PasswordHasher.hash_password(password)
        assert PasswordHasher.verify_password("mypassword", hashed) is False
        assert PasswordHasher.verify_password("MyPassword", hashed) is True

    def test_default_admin_hash_is_valid(self):
        """Test that default admin password hash is valid."""
        admin_hash = PasswordHasher.get_default_admin_hash()
        assert isinstance(admin_hash, str)
        assert "$" in admin_hash
        assert PasswordHasher.verify_password("admin123", admin_hash) is True

    def test_hash_with_special_characters(self):
        """Test hashing password with special characters."""
        password = "P@ssw0rd!#$%^&*()"
        hashed = PasswordHasher.hash_password(password)
        assert PasswordHasher.verify_password(password, hashed) is True

    def test_hash_with_unicode(self):
        """Test hashing password with unicode characters."""
        password = "pässwörd_日本語"
        hashed = PasswordHasher.hash_password(password)
        assert PasswordHasher.verify_password(password, hashed) is True
