class AppBaseException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

class ResourceNotFoundException(AppBaseException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, error_code="NOT_FOUND", status_code=404)

class ValidationException(AppBaseException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message=message, error_code="VALIDATION_ERROR", status_code=400)

class UnauthorizedException(AppBaseException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, error_code="UNAUTHORIZED", status_code=401)

class ForbiddenException(AppBaseException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, error_code="FORBIDDEN", status_code=403)