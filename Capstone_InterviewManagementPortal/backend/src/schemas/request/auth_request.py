"""Request schemas and validation rules for authentication workflows."""

import re

from pydantic import BaseModel, EmailStr, field_validator

from src.constants.app_constants import AppConstants


class LoginRequest(BaseModel):
    """Login request payload.

    Attributes:
        email: User email address accepted by Pydantic email validation.
        password: Plaintext password submitted for Basic credential matching.
    """

    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    """Password reset request payload with business validation rules.

    Attributes:
        email: Company email address for the account being updated.
        old_password: Current plaintext password used to authorize the reset.
        new_password: Replacement password validated against length and
            allowed-character rules.
    """

    email: EmailStr
    old_password: str
    new_password: str

    @field_validator('email')
    def validate_email_domain(cls, v):
        """Validate that password resets are limited to the company domain.

        Args:
            v: Email address parsed by Pydantic.

        Returns:
            EmailStr: Validated company email address.

        Raises:
            ValueError: If the email is outside the configured company domain.
        """
        if not v.endswith(f'@{AppConstants.DOMAIN_NAME}'):
            raise ValueError(f'Email must belong to {AppConstants.DOMAIN_NAME} domain')
        return v

    @field_validator('new_password')
    def validate_password(cls, v):
        """Validate password length and allowed characters.

        Args:
            v: Proposed replacement password.

        Returns:
            str: Validated replacement password.

        Raises:
            ValueError: If the password length or character set is invalid.
        """
        if not (AppConstants.PASSWORD_MIN_LENGTH <= len(v) <= AppConstants.PASSWORD_MAX_LENGTH):
            raise ValueError(f'Password must be between {AppConstants.PASSWORD_MIN_LENGTH} and {AppConstants.PASSWORD_MAX_LENGTH} characters')
        # Restrict the reset password to portable characters supported by the
        # current Basic Auth storage contract.
        if not re.match(r'^[A-Za-z0-9@#$%^&+=!_.-]+$', v):
            raise ValueError('Password contains invalid characters')
        return v
