"""Application-level exceptions."""


class ApplicationError(Exception):
    """Base application error class."""

    pass


class MockNotFoundError(ApplicationError):
    """Raised when a mock definition is not found."""

    pass


class InvalidJSONError(ApplicationError):
    """Raised when JSON data is invalid."""

    pass


class ValidationError(ApplicationError):
    """Raised when validation fails."""

    pass
