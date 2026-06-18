"""
22. Write a recursive function to calculate Fibonacci.
"""
# Constants
FIBONACCI_POSITION: int = 9

def calculate_recursive_fibonacci(n: int) -> int:
    """
    Calculates the nth Fibonacci number using recursion.
    """
    if n < 0:
        raise ValueError("Fibonacci sequence position cannot be negative.")
    
    # Base cases: fib(0) = 0, fib(1) = 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Recursive case: The sum of the two preceding numbers
    return calculate_recursive_fibonacci(n - 1) + calculate_recursive_fibonacci(n - 2)

if __name__ == "__main__":
    try:
        result: int = calculate_recursive_fibonacci(FIBONACCI_POSITION)
        print(f"The Fibonacci number at index {FIBONACCI_POSITION} is {result}.")
    except ValueError as e:
        print(f"Error: {e}")