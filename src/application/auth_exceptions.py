"""Authentication and authorization exceptions."""

from src.application.exceptions import ApplicationError


class AuthError(ApplicationError):
    """Base authentication error."""

    pass


class UnauthorizedError(AuthError):
    """Raised when user is not authenticated."""

    pass


class ForbiddenError(AuthError):
    """Raised when user lacks required permissions."""

    pass


class InvalidCredentialsError(AuthError):
    """Raised when credentials are invalid."""

    pass


class InvalidTokenError(AuthError):
    """Raised when token is invalid or expired."""

    pass
