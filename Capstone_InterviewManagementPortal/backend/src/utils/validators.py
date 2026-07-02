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
    normalized_email = email.strip().lower()
    if not NUCLEUSTEQ_EMAIL_PATTERN.fullmatch(normalized_email):
        raise ValueError(
            f"Email must be a valid {AppConstants.DOMAIN_NAME} address using only letters, numbers, and single periods in the local part"
        )
    return normalized_email


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
