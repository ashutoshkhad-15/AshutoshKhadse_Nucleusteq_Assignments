"""Custom exception types used to produce standardized API errors."""


class AppBaseException(Exception):
    """Base exception carrying API error response metadata.

    Args:
        message: Human-readable error message returned to the client.
        error_code: Stable machine-readable error code.
        status_code: HTTP status code used by the exception handler.
    """

    def __init__(self, message: str, error_code: str, status_code: int):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class ResourceNotFoundException(AppBaseException):
    """Exception raised when a requested resource cannot be found."""

    def __init__(self, message: str = "Resource not found"):
        """Initialize a not-found exception.

        Args:
            message: Client-facing not-found message.
        """
        super().__init__(message=message, error_code="NOT_FOUND", status_code=404)


class ValidationException(AppBaseException):
    """Exception raised when business validation fails."""

    def __init__(self, message: str = "Validation failed"):
        """Initialize a validation exception.

        Args:
            message: Client-facing validation failure message.
        """
        super().__init__(message=message, error_code="VALIDATION_ERROR", status_code=400)


class UnauthorizedException(AppBaseException):
    """Exception raised when authentication is missing or invalid."""

    def __init__(self, message: str = "Authentication required"):
        """Initialize an unauthorized exception.

        Args:
            message: Client-facing authentication error message.
        """
        super().__init__(message=message, error_code="UNAUTHORIZED", status_code=401)


class ForbiddenException(AppBaseException):
    """Exception raised when an authenticated user lacks permission."""

    def __init__(self, message: str = "Permission denied"):
        """Initialize a forbidden exception.

        Args:
            message: Client-facing authorization error message.
        """
        super().__init__(message=message, error_code="FORBIDDEN", status_code=403)
