"""Request schemas and validation rules for authentication workflows."""

import re

from pydantic import BaseModel, EmailStr, field_validator

from src.constants.app_constants import AppConstants


PASSWORD_ALLOWED_CHARACTERS = re.compile(r'^[A-Za-z0-9@#$%^&+=!_.-]+$')


def _validate_company_email(email: EmailStr) -> EmailStr:
    """Ensure the authentication flow only accepts company email addresses."""
    if not email.endswith(f'@{AppConstants.DOMAIN_NAME}'):
        raise ValueError(f'Email must belong to {AppConstants.DOMAIN_NAME} domain')
    return email


def _validate_password_policy(password: str) -> str:
    """Validate the supported password length and character set."""
    if not (AppConstants.PASSWORD_MIN_LENGTH <= len(password) <= AppConstants.PASSWORD_MAX_LENGTH):
        raise ValueError(
            f'Password must be between {AppConstants.PASSWORD_MIN_LENGTH} and {AppConstants.PASSWORD_MAX_LENGTH} characters'
        )
    if not PASSWORD_ALLOWED_CHARACTERS.fullmatch(password):
        raise ValueError('Password contains invalid characters')
    return password


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
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        """Validate that password resets are limited to the company domain."""
        return _validate_company_email(value)

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate password length and allowed characters."""
        return _validate_password_policy(value)
