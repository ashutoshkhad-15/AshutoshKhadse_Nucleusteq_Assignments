"""API routes for administrative user management operations."""

import logging

from fastapi import APIRouter, Depends

from src.enums.app_enums import UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.user_service import UserService
from src.utils.security import require_role

logger = logging.getLogger(__name__)

# Only ADMIN can manage users.
router = APIRouter(
    prefix="/users", 
    tags=["User Management"],
    dependencies=[Depends(require_role([UserRole.ADMIN.value]))]
)

@router.post("/", response_model=SuccessResponse[dict])
async def create_user(request: CreateUserRequest):
    """Create a user account through the admin-only management endpoint."""
    user_service = UserService()
    try:
        data = await user_service.create_user(request)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while creating user through API")
        raise
    return SuccessResponse(message="User created successfully", data=data)

@router.get("/", response_model=SuccessResponse[list])
async def get_users(search: str | None = None):
    """Retrieve all managed users or a filtered subset when a search term is provided."""
    user_service = UserService()
    try:
        data = await user_service.get_all_users(search=search)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while retrieving users through API")
        raise
    return SuccessResponse(message="Users retrieved successfully", data=data)

@router.get("/{user_id}", response_model=SuccessResponse[dict])
async def get_user_by_id(user_id: str):
    """Retrieve a single user by identifier."""
    user_service = UserService()
    try:
        data = await user_service.get_user_by_id(user_id)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while retrieving user %s through API", user_id)
        raise
    return SuccessResponse(message="User retrieved successfully", data=data)

@router.patch("/{user_id}", response_model=SuccessResponse[dict])
async def update_user(user_id: str, request: UpdateUserRequest):
    """Apply partial updates to an existing user account."""
    user_service = UserService()
    try:
        data = await user_service.update_user(user_id, request)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while updating user %s through API", user_id)
        raise
    return SuccessResponse(message="User updated successfully", data=data)

@router.patch("/{user_id}/disable", response_model=SuccessResponse[None])
async def disable_user(user_id: str):
    """Disable a user account through the administrative endpoint."""
    user_service = UserService()
    try:
        await user_service.disable_user(user_id)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while disabling user %s through API", user_id)
        raise
    return SuccessResponse(message="User disabled successfully")