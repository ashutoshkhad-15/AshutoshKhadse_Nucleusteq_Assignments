"""
17. Write a lambda function to find the square of a number.
"""
from typing import Callable

# Constants
TEST_NUMBER: int = 8

def demonstrate_lambda_square() -> None:
    """Demonstrates the use of a lambda function to calculate a square."""
    
    # Defining the lambda function with typing (takes an int, returns an int)
    calculate_square: Callable[[int], int] = lambda x: x ** 2
    
    result: int = calculate_square(TEST_NUMBER)
    print(f"The square of {TEST_NUMBER} is {result}.")

if __name__ == "__main__":
    demonstrate_lambda_square()