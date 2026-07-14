"""User response DTOs."""

from pydantic import BaseModel

from src.enums.app_enums import UserRole


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    is_active: bool
    requires_password_reset: bool

