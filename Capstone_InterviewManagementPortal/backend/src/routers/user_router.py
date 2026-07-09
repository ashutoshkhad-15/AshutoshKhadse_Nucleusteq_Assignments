"""API routes for administrative user management operations."""

import logging

from fastapi import APIRouter, Depends, Query

from src.enums.app_enums import UserRole
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.user_service import UserService
from src.utils.dependencies import get_user_service
from src.utils.security import require_role

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
    dependencies=[Depends(require_role([UserRole.ADMIN.value]))]
)

@router.post("/", response_model=SuccessResponse[dict])
async def create_user(request: CreateUserRequest, user_service: UserService = Depends(get_user_service)):
    """Create a user account through the admin-only management endpoint."""
    data = await user_service.create_user(request)
    return SuccessResponse(message="User created successfully", data=data)

@router.get("/", response_model=SuccessResponse[list])
async def get_users(search: str | None = None, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), user_service: UserService = Depends(get_user_service)):
    """Retrieve all managed users or a filtered subset when a search term is provided."""
    data, meta = await user_service.get_all_users(search=search, page=page, limit=limit)
    return SuccessResponse(message="Users retrieved successfully", data=data, meta=meta)

@router.get("/{user_id}", response_model=SuccessResponse[dict])
async def get_user_by_id(user_id: str, user_service: UserService = Depends(get_user_service)):
    """Retrieve a single user by identifier."""
    data = await user_service.get_user_by_id(user_id)
    return SuccessResponse(message="User retrieved successfully", data=data)

@router.patch("/{user_id}", response_model=SuccessResponse[dict])
async def update_user(user_id: str, request: UpdateUserRequest, user_service: UserService = Depends(get_user_service)):
    """Apply partial updates to an existing user account."""
    data = await user_service.update_user(user_id, request)
    return SuccessResponse(message="User updated successfully", data=data)

@router.patch("/{user_id}/disable", response_model=SuccessResponse[None])
async def disable_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    """Disable a user account through the administrative endpoint."""
    await user_service.disable_user(user_id)
    return SuccessResponse(message="User disabled successfully")
