"""
26. Write a regular expression to validate a 10-digit mobile number.
"""
import re

# Constants
# Matches exactly 10 digits from start (^) to end ($)
MOBILE_PATTERN: str = r'^\d{10}$'
TEST_NUMBERS: list[str] = ["9876543210", "12345", "987654321099", "abc4567890"]

def is_valid_mobile_number(number: str) -> bool:
    """
    Checks if a given string contains exactly 10 digits and nothing else.
    """
    # re.fullmatch ensures the entire string matches the pattern, 
    # making it ideal for exact length/format validations.
    return bool(re.fullmatch(MOBILE_PATTERN, number))

if __name__ == "__main__":
    for mobile in TEST_NUMBERS:
        validity: str = "Valid" if is_valid_mobile_number(mobile) else "Invalid"
        print(f"[{validity}] {mobile}")