"""Authentication API routes for login, password reset, and logout."""

from fastapi import APIRouter, Depends

from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.auth_service import AuthService
from src.utils.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=SuccessResponse[dict])
async def login(request: LoginRequest):
    """Authenticate a user with email and password credentials.

    The endpoint expects a JSON request body containing a valid email address
    and plaintext password. No authorization header is required. On success, it
    returns the authenticated user's email, role, and password-reset status.

    Args:
        request: Login credentials submitted by the client.

    Returns:
        SuccessResponse[dict]: Authentication result wrapped in the shared
        success envelope.

    Raises:
        UnauthorizedException: If credentials are invalid or the account is
            disabled.
    """
    auth_service = AuthService()
    data = await auth_service.login(request)
    return SuccessResponse(message="Login successful", data=data)


@router.post("/reset-password", response_model=SuccessResponse[None])
async def reset_password(request: ResetPasswordRequest):
    """Reset a user's password after validating the old password.

    The endpoint expects a JSON request body containing the user's company
    email, current password, and compliant replacement password. No
    authorization header is required because the old password is validated as
    part of the request.

    Args:
        request: Password reset request payload.

    Returns:
        SuccessResponse[None]: Success envelope with no response data.

    Raises:
        UnauthorizedException: If the email or current password is invalid.
        RequestValidationError: If the email domain or new password rules fail.
    """
    auth_service = AuthService()
    await auth_service.reset_password(request)
    return SuccessResponse(message="Password reset successfully")


@router.post("/logout", response_model=SuccessResponse[None])
async def logout(current_user: dict = Depends(get_current_user)):
    """Validate the current Basic Auth session before logout.

    The endpoint requires a valid HTTP Basic Authorization header. Because
    Basic Auth is stateless, server-side logout does not revoke a session; the
    response instructs the client to clear stored credentials after the server
    confirms the user is still valid.

    Args:
        current_user: Authenticated user document resolved by the security
            dependency.

    Returns:
        SuccessResponse[None]: Success envelope indicating client-side
        credential cleanup can proceed.

    Raises:
        UnauthorizedException: If credentials are missing or invalid.
        ForbiddenException: If the account is disabled.
        AppBaseException: If a password reset is required before protected
            access is granted.
    """
    return SuccessResponse(
        message="Logout successful. Please clear client credentials."
    )
