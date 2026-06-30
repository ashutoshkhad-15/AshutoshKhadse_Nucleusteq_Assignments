"""Request schemas for user management endpoints."""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from src.constants.app_constants import AppConstants
from src.enums.app_enums import UserRole

class CreateUserRequest(BaseModel):
    """Validate the data required to create a new user account."""

    email: EmailStr
    role: UserRole

    @field_validator('email')
    def validate_email_domain(cls, v):
        # Restrict account creation to the organization's email domain.
        if not v.endswith(f'@{AppConstants.DOMAIN_NAME}'):
            raise ValueError(f'Email must belong to {AppConstants.DOMAIN_NAME} domain')
        return v

class UpdateUserRequest(BaseModel):
    """Capture optional fields that can be updated for an existing user."""

    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
