"""
7. Create a custom exception called AgeException and raise it if age is less than 18.
"""

# Constants
MINIMUM_AGE_REQUIRED: int = 18
USER_AGE_INPUT: int = 16

class AgeException(Exception):
    """Custom exception raised when a user does not meet the age requirement."""
    def __init__(self, message: str = "Age is less than 18. Access denied.") -> None:
        self.message = message
        super().__init__(self.message)

def verify_age(age: int) -> None:
    """
    Checks the user's age and raises AgeException if under the minimum requirement.
    """
    if age < MINIMUM_AGE_REQUIRED:
        raise AgeException(f"Age {age} is below the required {MINIMUM_AGE_REQUIRED}.")
    print("Age verified. Access granted.")

if __name__ == "__main__":
    try:
        verify_age(USER_AGE_INPUT)
    except AgeException as ae:
        print(f"Verification Failed: {ae}")