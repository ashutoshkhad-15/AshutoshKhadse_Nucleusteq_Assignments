"""Authentication service for credential validation and password resets."""

from src.repositories.user_repository import UserRepository
from src.utils.security import encode_password
from src.exceptions.custom_exceptions import UnauthorizedException
from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest


class AuthService:
    """Coordinate authentication business rules with user persistence."""

    def __init__(self):
        """Initialize the service with the user repository dependency."""
        self.user_repo = UserRepository()

    async def login(self, request: LoginRequest) -> dict:
        """Authenticate a user and return session metadata.

        The method validates the submitted email and password against the
        stored Base64-encoded password value. Disabled accounts are rejected
        even when credentials match.

        Args:
            request: Login request containing email and plaintext password.

        Returns:
            dict: Authenticated user email, role, and password-reset flag.

        Raises:
            UnauthorizedException: If the user does not exist, the password is
                invalid, or the account is disabled.
        """
        user = await self.user_repo.get_user_by_email(request.email)
        if not user or user.get("password_base64") != encode_password(request.password):
            raise UnauthorizedException("Invalid email or password")
        
        if not user.get("is_active", True):
            raise UnauthorizedException("Account is disabled")

        return {
            "email": user["email"],
            "role": user["role"],
            "requires_password_reset": user.get("requires_password_reset", False)
        }

    async def reset_password(self, request: ResetPasswordRequest):
        """Reset a user's password after verifying the current password.

        The request schema enforces email-domain and password-format rules
        before this method runs. The service verifies the current password,
        stores the replacement password using the configured encoding scheme,
        and clears the first-login reset flag.

        Args:
            request: Password reset request containing email, old password, and
                new password.

        Returns:
            None: Password fields are updated through the repository.

        Raises:
            UnauthorizedException: If the user does not exist or the old
                password does not match the stored password.
        """
        user = await self.user_repo.get_user_by_email(request.email)
        if not user or user.get("password_base64") != encode_password(request.old_password):
            raise UnauthorizedException("Invalid email or old password")

        new_password_encoded = encode_password(request.new_password)
        await self.user_repo.update_user(
            email=request.email,
            update_data={
                "password_base64": new_password_encoded,
                "requires_password_reset": False
            }
        )
