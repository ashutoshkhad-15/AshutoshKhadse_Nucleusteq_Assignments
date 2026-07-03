"""Service layer for user management workflows."""

import logging

from src.core.config import settings
from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.user_repository import UserRepository
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.utils.security import encode_password

logger = logging.getLogger(__name__)


class UserService:
    """Coordinate user-related business rules and persistence operations."""

    def __init__(self):
        """Initialize the service with the user repository dependency."""
        self.user_repo = UserRepository()

    async def create_user(self, request: CreateUserRequest) -> dict:
        """Create a new user with the default temporary password."""
        try:
            existing_user = await self.user_repo.get_user_by_email(request.email)
        except Exception:
            logger.exception("Repository failure while checking duplicate email for user: %s", request.email)
            raise

        if existing_user:
            logger.warning("Duplicate email detected while creating user: %s", request.email)
            raise AppBaseException("User with this email already exists", "USER_EXISTS", 400)

        default_password = settings.DEFAULT_USER_PASSWORD

        if not default_password:
            logger.error("Missing default password configuration while creating user: %s", request.email)
            raise AppBaseException(
                "Server misconfiguration: DEFAULT_USER_PASSWORD environment variable is missing.",
                "SERVER_ERROR",
                500,
            )

        user_data = {
            "email": request.email,
            "password_base64": encode_password(default_password),
            "role": request.role.value,
            "is_active": True,
            "requires_password_reset": True,
        }

        try:
            result = await self.user_repo.create_user(user_data)
        except Exception:
            logger.exception("Repository failure while creating user: %s", request.email)
            raise

        result.pop("password_base64", None)
        logger.info("User created successfully: %s", request.email)
        return result

    async def get_all_users(self, search: str | None = None) -> list:
        """Return all users or a filtered subset when a search term is provided."""
        search_term = (search or "").strip().lower()
        if search_term:
            logger.info("Searching users with term: %s", search_term)
            try:
                users = await self.user_repo.search_users(search_term)
            except Exception:
                logger.exception("Repository failure while searching users")
                raise
            logger.info("User search completed successfully")
            return users

        try:
            users = await self.user_repo.get_all_users()
        except Exception:
            logger.exception("Repository failure while fetching all users")
            raise

        logger.info("User list retrieved successfully")
        return users

    async def get_user_by_id(self, user_id: str) -> dict:
        """Return a single user record or raise if it does not exist."""
        try:
            user = await self.user_repo.get_user_by_id(user_id)
        except Exception:
            logger.exception("Repository failure while fetching user by ID: %s", user_id)
            raise

        if not user:
            logger.warning("User not found for ID: %s", user_id)
            raise AppBaseException("User not found", "USER_NOT_FOUND", 404)

        logger.info("User retrieved successfully: %s", user_id)
        return user

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> dict:
        """Apply partial updates to an existing user record."""
        await self.get_user_by_id(user_id)

        update_data = {k: v for k, v in request.model_dump().items() if v is not None}
        if not update_data:
            logger.warning("Invalid update request for user ID: %s", user_id)
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)

        try:
            await self.user_repo.update_user_by_id(user_id, update_data)
        except Exception:
            logger.exception("Repository failure while updating user by ID: %s", user_id)
            raise

        logger.info("User updated successfully: %s", user_id)
        return await self.get_user_by_id(user_id)

    async def disable_user(self, user_id: str):
        """Disable a user account while protecting the primary super-admin."""
        user = await self.get_user_by_id(user_id)
        if user["email"] == "admin@nucleusteq.com":
            logger.warning("Unauthorized disable attempt for primary admin user ID: %s", user_id)
            raise AppBaseException("Cannot disable the primary super admin", "ACTION_DENIED", 403)

        try:
            await self.user_repo.update_user_by_id(user_id, {"is_active": False})
        except Exception:
            logger.exception("Repository failure while disabling user: %s", user_id)
            raise

        logger.info("User disabled successfully: %s", user_id)
