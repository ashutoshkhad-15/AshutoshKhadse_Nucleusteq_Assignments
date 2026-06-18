"""
25. Write a regular expression to validate an email address.
"""
import re

# Constants
EMAIL_PATTERN: str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
TEST_EMAILS: list[str] = ["user@example.com", "invalid-email.com", "admin@domain.co.in"]

def is_valid_email(email: str) -> bool:
    """
    Validates the structure of an email address using a standard regex pattern.
    """
    # re.match checks for a match only at the beginning of the string.
    # Because our pattern starts with ^ and ends with $, it forces a full string match.
    match_found = re.match(EMAIL_PATTERN, email)
    return bool(match_found)

if __name__ == "__main__":
    for test_email in TEST_EMAILS:
        validity: str = "Valid" if is_valid_email(test_email) else "Invalid"
        print(f"[{validity}] {test_email}")