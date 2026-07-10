"""Reusable validation helpers shared across request schemas."""

import re

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
    normalized_email = normalize_email(email)
    if not NUCLEUSTEQ_EMAIL_PATTERN.fullmatch(normalized_email):
        raise ValueError(
            f"Email must be a valid {AppConstants.DOMAIN_NAME} address using only letters, numbers, and single periods in the local part"
        )
    return normalized_email


def normalize_email(email: str) -> str:
    """Return a trimmed, lowercase email string."""
    return email.strip().lower()


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

JOB_EXPERIENCE_PATTERN = re.compile(
    r"^(?:\d{1,2}\s+year|\d{1,2}\s+years|\d{1,2}\+\s+years|\d{1,2}-\d{1,2}\s+years)$"
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


def normalize_required_text(value: str, field_name: str, min_length: int, max_length: int) -> str:
    """Normalize a required text field and validate its size bounds."""
    normalized_value = validate_required_text(value, field_name)
    if len(normalized_value) < min_length or len(normalized_value) > max_length:
        raise ValueError(f"{field_name} must be between {min_length} and {max_length} characters")
    return normalized_value


def normalize_text_with_pattern(
    value: str,
    field_name: str,
    min_length: int,
    max_length: int,
    pattern: re.Pattern[str],
    invalid_message: str,
    allow_multiple_spaces: bool = True,
) -> str:
    """Normalize a text field and enforce a content pattern."""
    normalized_value = validate_required_text(value, field_name)
    normalized_value = re.sub(r"\s+", " ", normalized_value).strip() if allow_multiple_spaces else normalized_value
    if len(normalized_value) < min_length or len(normalized_value) > max_length:
        raise ValueError(f"{field_name} must be between {min_length} and {max_length} characters")
    if not pattern.fullmatch(normalized_value):
        raise ValueError(invalid_message)
    return normalized_value


def normalize_skill_text(value: str) -> str:
    """Normalize and validate a single skill chip value."""
    normalized = validate_required_text(value, "Skill")
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if len(normalized) < 2 or len(normalized) > 30:
        raise ValueError("Skill must be between 2 and 30 characters")
    if not re.search(r"[A-Za-z]", normalized):
        raise ValueError("Skill must contain at least one alphabetic character")
    if not re.fullmatch(r"[A-Za-z0-9 .&()/+\-]+", normalized):
        raise ValueError("Skill can contain letters, numbers, spaces, and common symbols only")
    return normalized


def normalize_string_list(values) -> list[str]:
    """Trim, deduplicate, and discard empty values from a string list."""
    normalized: list[str] = []
    for value in values or []:
        if not isinstance(value, str):
            continue
        item = value.strip()
        if not item:
            continue
        if item.lower() not in {existing.lower() for existing in normalized}:
            normalized.append(item)
    return normalized
