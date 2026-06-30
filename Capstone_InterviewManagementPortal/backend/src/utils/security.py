"""Security helpers and FastAPI dependencies for Basic authentication."""

import base64

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.exceptions.custom_exceptions import UnauthorizedException, ForbiddenException, AppBaseException
from src.repositories.user_repository import UserRepository

security = HTTPBasic()


def encode_password(password: str) -> str:
    """Encode a plaintext password using the configured Base64 contract.

    Args:
        password: Plaintext password supplied by the client or seed script.

    Returns:
        str: UTF-8 Base64 encoded password string.
    """
    return base64.b64encode(password.encode('utf-8')).decode('utf-8')


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Resolve and validate the current user from HTTP Basic credentials.

    This dependency authenticates protected routes by comparing the submitted
    password with the stored Base64-encoded password value. It also enforces
    account status and first-login reset requirements before allowing access.

    Args:
        credentials: HTTP Basic credentials extracted by FastAPI.

    Returns:
        dict: Authenticated user document from the users collection.

    Raises:
        UnauthorizedException: If the email or password is invalid.
        ForbiddenException: If the user account is disabled.
        AppBaseException: If the user must reset the password before access.
    """
    user_repo = UserRepository()
    user = await user_repo.get_user_by_email(credentials.username)
    
    if not user or user.get("password_base64") != encode_password(credentials.password):
        raise UnauthorizedException("Invalid email or password")
        
    if not user.get("is_active", True):
        raise ForbiddenException("User account is disabled")
        
    if user.get("requires_password_reset", False):
        # Prevent access to protected resources until the seeded or temporary
        # password has been replaced.
        raise AppBaseException(
            message="Password reset required at first login", 
            error_code="PASSWORD_RESET_REQUIRED", 
            status_code=403
        )
        
    return user
