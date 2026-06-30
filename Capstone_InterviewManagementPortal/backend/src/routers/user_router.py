from fastapi import APIRouter, Depends
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.user_service import UserService
from src.utils.security import require_role
from src.enums.app_enums import UserRole

# Only ADMIN can manage users. 
router = APIRouter(
    prefix="/users", 
    tags=["User Management"],
    dependencies=[Depends(require_role([UserRole.ADMIN.value]))]
)

@router.post("/", response_model=SuccessResponse[dict])
async def create_user(request: CreateUserRequest):
    user_service = UserService()
    data = await user_service.create_user(request)
    return SuccessResponse(message="User created successfully", data=data)

@router.get("/", response_model=SuccessResponse[list])
async def get_users():
    user_service = UserService()
    data = await user_service.get_all_users()
    return SuccessResponse(message="Users retrieved successfully", data=data)

@router.get("/{user_id}", response_model=SuccessResponse[dict])
async def get_user_by_id(user_id: str):
    user_service = UserService()
    data = await user_service.get_user_by_id(user_id)
    return SuccessResponse(message="User retrieved successfully", data=data)

@router.patch("/{user_id}", response_model=SuccessResponse[dict])
async def update_user(user_id: str, request: UpdateUserRequest):
    user_service = UserService()
    data = await user_service.update_user(user_id, request)
    return SuccessResponse(message="User updated successfully", data=data)

@router.patch("/{user_id}/disable", response_model=SuccessResponse[None])
async def disable_user(user_id: str):
    user_service = UserService()
    await user_service.disable_user(user_id)
    return SuccessResponse(message="User disabled successfully")