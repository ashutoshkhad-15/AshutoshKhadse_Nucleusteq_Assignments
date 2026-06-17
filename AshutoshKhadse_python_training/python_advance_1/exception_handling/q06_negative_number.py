"""
6. Create a function that raises a ValueError if a number is negative.
"""
# Constants
TEST_NUMBER: int = -10 

def validate_positive_number(number: int) -> None:
    """
    Validates that a number is positive. Raises a ValueError otherwise.
    """
    if number < 0:
        raise ValueError(f"Invalid input: {number}. Number cannot be negative.")
    print(f"Validation passed for number: {number}")

if __name__ == "__main__":
    try:
        validate_positive_number(TEST_NUMBER)
    except ValueError as ve:
        print(f"Caught Exception: {ve}")