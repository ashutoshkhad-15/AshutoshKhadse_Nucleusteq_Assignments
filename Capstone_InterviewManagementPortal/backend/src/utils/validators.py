"""Reusable validation helpers shared across request schemas."""

import re
from dataclasses import dataclass

from src.constants.app_constants import AppConstants


NUCLEUSTEQ_EMAIL_PATTERN = re.compile(
    rf"^(?!\.)(?!.*\.\.)([A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)@{re.escape(AppConstants.DOMAIN_NAME)}$"
)


def validate_nucleusteq_email(email: str) -> str:
    """Validate the strict corporate email format used by candidate flows.

    Args:
        email: Email address supplied by the client.

    Returns:
        str: The validated email address.

    Raises:
        ValueError: If the email does not match the required company format.
    """
    normalized_email = email.strip().lower()
    if not NUCLEUSTEQ_EMAIL_PATTERN.fullmatch(normalized_email):
        raise ValueError(
            f"Email must be a valid {AppConstants.DOMAIN_NAME} address using only letters, numbers, and single periods in the local part"
        )
    return normalized_email


def validate_required_text(value: str, field_name: str) -> str:
    """Normalize a required text field and reject empty values."""
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} is required")
    return normalized_value


def validate_mobile_number(mobile: str) -> str:
    """Validate a mobile number against the project-standard numeric format.

    Args:
        mobile: Mobile number supplied by the client.

    Returns:
        str: The validated mobile number.

    Raises:
        ValueError: If the mobile number is not numeric or has an invalid length.
    """
    normalized_mobile = mobile.strip()
    if not normalized_mobile.isdigit():
        raise ValueError("Mobile number must contain digits only")
    if len(normalized_mobile) != AppConstants.MOBILE_NUMBER_LENGTH:
        raise ValueError(
            f"Mobile number must be {AppConstants.MOBILE_NUMBER_LENGTH} digits long"
        )
    return normalized_mobile


EXPERIENCE_PATTERN = re.compile(
    r"^(?:(?P<years>\d{1,2})(?:\+)?\s+years?|(?P<months>\d{1,2})\s+months?)$",
    re.IGNORECASE,
)


def validate_experience_text(experience: str) -> str:
    """Validate a human-readable experience string such as '3 years' or '6 months'."""
    normalized = experience.strip().lower()
    match = EXPERIENCE_PATTERN.fullmatch(normalized)
    if not match:
        raise ValueError("Experience must be formatted as '0 years', '3 years', '4+ years', or '6 months'")

    years = match.group("years")
    months = match.group("months")
    if years is not None:
        value = int(years)
        if value < 0 or value > 50:
            raise ValueError("Years of experience must be between 0 and 50")
    if months is not None:
        value = int(months)
        if value < 1 or value > 11:
            raise ValueError("Months of experience must be between 1 and 11")
    return normalized
