"""
31. Create a password validation program using regex (minimum length, one digit, one special character).16 min length
"""
import re

# Constants
# (?=.*\d) checks for at least one digit.
# (?=.*[^a-zA-Z0-9\s]) checks for at least one non-alphanumeric char (special char).
# .{16,} ensures the total length is 16 or more.
PASSWORD_PATTERN: str = r'^(?=.*\d)(?=.*[^a-zA-Z0-9\s]).{16,}$'

TEST_PASSWORDS: list[str] = [
    "Short1!",                     # Invalid: Too short
    "ThisIsALongPasswordWithout",  # Invalid: No digits or special chars
    "ThisIsALongPass12345",        # Invalid: No special char
    "SecureP@ssw0rdFor2024!!!",    # Valid: >16 chars, has digit, has special char
]

def is_strong_password(password: str) -> bool:
    """
    Validates a password based on strict criteria: 
    - Minimum 16 characters long.
    - Contains at least one digit.
    - Contains at least one special character.
    """
    return bool(re.match(PASSWORD_PATTERN, password))

if __name__ == "__main__":
    for pwd in TEST_PASSWORDS:
        validity: str = "Passed" if is_strong_password(pwd) else "Failed"
        print(f"[{validity}] {pwd}")