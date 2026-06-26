"""Service layer for user management workflows."""

import os

from src.core.config import settings
from src.repositories.user_repository import UserRepository
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.utils.security import encode_password
from src.exceptions.custom_exceptions import AppBaseException

class UserService:
    """Coordinate user-related business rules and persistence operations."""

    def __init__(self):
        """Initialize the service with the user repository dependency."""
        self.user_repo = UserRepository()

    async def create_user(self, request: CreateUserRequest) -> dict:
        """Create a new user with the default temporary password."""
        existing_user = await self.user_repo.get_user_by_email(request.email)
        if existing_user:
            raise AppBaseException("User with this email already exists", "USER_EXISTS", 400)
        
        default_password = settings.DEFAULT_USER_PASSWORD
        
        if not default_password:
            # If the .env is missing, block the creation and alert the IT team.
            raise AppBaseException(
                "Server misconfiguration: DEFAULT_USER_PASSWORD environment variable is missing.", 
                "SERVER_ERROR", 
                500
            )
            
        user_data = {
            "email": request.email,
            "password_base64": encode_password(default_password),
            "role": request.role.value,
            "is_active": True,
            "requires_password_reset": True 
        }
        
        result = await self.user_repo.create_user(user_data)
        # Never return the password to the frontend.
        del result["password_base64"]
        return result

    async def get_all_users(self) -> list:
        """Return all users visible to the current caller."""
        return await self.user_repo.get_all_users()

    async def get_user_by_id(self, user_id: str) -> dict:
        """Return a single user record or raise if it does not exist."""
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise AppBaseException("User not found", "USER_NOT_FOUND", 404)
        return user

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> dict:
        """Apply partial updates to an existing user record."""
        # Validate existence before applying a partial update.
        await self.get_user_by_id(user_id)
        
        update_data = {k: v for k, v in request.model_dump().items() if v is not None}
        if not update_data:
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)
            
        await self.user_repo.update_user_by_id(user_id, update_data)
        return await self.get_user_by_id(user_id)

    async def disable_user(self, user_id: str):
        """Disable a user account while protecting the primary super-admin."""
        user = await self.get_user_by_id(user_id)
        if user["email"] == "admin@nucleusteq.com":
            raise AppBaseException("Cannot disable the primary super admin", "ACTION_DENIED", 403)
            
        await self.user_repo.update_user_by_id(user_id, {"is_active": False})
