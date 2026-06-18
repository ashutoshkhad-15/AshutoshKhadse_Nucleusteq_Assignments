"""
21. Write a recursive function to calculate factorial.
"""
# Constants
TARGET_FACTORIAL: int = 7

def calculate_factorial(n: int) -> int:
    """
    Calculates the factorial of a number using recursion.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    # Base cases: 0! or 1! is 1
    if n in (0, 1):
        return 1
    
    # Recursive case
    return n * calculate_factorial(n - 1)

if __name__ == "__main__":
    try:
        result: int = calculate_factorial(TARGET_FACTORIAL)
        print(f"The factorial of {TARGET_FACTORIAL} is {result}.")
    except ValueError as e:
        print(f"Error: {e}")