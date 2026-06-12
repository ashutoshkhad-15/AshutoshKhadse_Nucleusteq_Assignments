"""
Module   : q14_factorial_calculator.py
Package  : python_basic.loops
Topics   : Python Basics – Loops
Question 14: Find factorial of a number.
"""

def calculate_factorial(number: int) -> int:
    """
    Calculates the factorial of a positive integer using an iterative loop.
    """
    # Guard clause to handle edge cases immediately without executing loop logic
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if number == 0 or number == 1:
        return 1

    factorial_result: int = 1
    
    # We use a bottom-up iterative approach (O(n) time complexity).
    for i in range(2, number + 1):
        factorial_result *= i
        
    return factorial_result

def execute_factorial_program() -> None:
    """
    Handles input and outputs the calculated factorial.
    """
    val: int = int(input("Enter a positive integer: "))
    
    try:
        result: int = calculate_factorial(val)
        print(f"The factorial of {val} ({val}!) is {result}")
    except ValueError as error_msg:
        print(f"Error: {error_msg}")

if __name__ == "__main__":
    execute_factorial_program()