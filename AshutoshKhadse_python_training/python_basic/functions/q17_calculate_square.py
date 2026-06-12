"""
Module   : q17_calculate_square.py
Package  : python_basic.functions
Topics   : Functions
Question 17: Write a function to calculate square of a number.
"""

def calculate_square(number: float) -> float:
    """
    Calculates and returns the square of a given numerical value.
     Args:
        number : The value to square.

    Returns:
        number ** 2
    """
    # The exponentiation operator (**) is highly optimized in Python 
    # compared to manually multiplying the number by itself.
    return number ** 2

def execute_square_calculator() -> None:
    """
    Handles user input, displays the squared result, and safely catches invalid types.
    """
    
    # A while loop combined with a try-except block forces the program to keep asking
    # until the user provides a mathematically valid float, preventing runtime crashes.
    while True:
        try:
            val: float = float(input("Enter a number to square: "))
            squared_result: float = calculate_square(val)
            print(f"The square of {val} is {squared_result}")
            break  # Exit the loop upon successful calculation
            
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value (e.g., 5 or 4.2).")

if __name__ == "__main__":
    execute_square_calculator()