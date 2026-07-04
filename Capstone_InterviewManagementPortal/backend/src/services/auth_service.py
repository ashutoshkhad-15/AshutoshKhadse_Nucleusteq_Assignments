"""Authentication service for credential validation and password resets."""

import logging

from src.repositories.user_repository import UserRepository
from src.utils.security import encode_password
from src.exceptions.custom_exceptions import UnauthorizedException
from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest

logger = logging.getLogger(__name__)


class AuthService:
    """Coordinate authentication business rules with user persistence."""

    def __init__(self):
        """Initialize the service with the user repository dependency."""
        self.user_repo = UserRepository()

    async def _get_user_by_email(self, email: str, context: str) -> dict | None:
        """Load a user record and preserve repository error handling context."""
        try:
            return await self.user_repo.get_user_by_email(email)
        except Exception:
            logger.exception("Repository failure while %s user: %s", context, email)
            raise

    @staticmethod
    def _is_valid_password(user: dict | None, password: str) -> bool:
        """Compare an incoming password against the stored encoded value."""
        return bool(user) and user.get("password_base64") == encode_password(password)

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
        user = await self._get_user_by_email(request.email, "fetching user for login")

        if not self._is_valid_password(user, request.password):
            logger.warning("Invalid login attempt for email: %s", request.email)
            raise UnauthorizedException("Invalid email or password")

        if not user.get("is_active", True):
            logger.warning("Login attempt rejected for disabled account: %s", request.email)
            raise UnauthorizedException("Account is disabled")

        logger.info("Successful login for user: %s", request.email)
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
        user = await self._get_user_by_email(request.email, "fetching user for reset-password")

        if not self._is_valid_password(user, request.old_password):
            logger.warning("Password reset attempt failed for user: %s", request.email)
            raise UnauthorizedException("Invalid email or old password")

        new_password_encoded = encode_password(request.new_password)
        try:
            await self.user_repo.update_user(
                email=request.email,
                update_data={
                    "password_base64": new_password_encoded,
                    "requires_password_reset": False,
                },
            )
        except Exception:
            logger.exception("Repository failure while updating password for user: %s", request.email)
            raise

        logger.info("Password reset completed for user: %s", request.email)
