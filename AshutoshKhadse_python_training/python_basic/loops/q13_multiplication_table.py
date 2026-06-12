"""
Module   : q13_multiplication_table.py
Package  : python_basic.loops
Topics   : Python Basics – Loops
Question 13: Print multiplication table of a number.
"""

def print_multiplication_table(number: int, up_to: int = 10) -> None:
    """
    Generates and prints a formatted multiplication table for a given integer.
    """
    print(f" Multiplication Table for {number} ")
    
    # Time complexity is O(n) where n is the 'up_to' parameter.
    for multiplier in range(1, up_to + 1):
        product: int = number * multiplier
        # f-strings allow us to perfectly align the table visually
        print(f"{number} x {multiplier:<2} = {product}")

def execute_table_generator() -> None:
    """
    Captures user input and executes the table generation logic.
    """
    user_num: int = int(input("Enter an integer to generate its multiplication table: "))
    print_multiplication_table(user_num)

if __name__ == "__main__":
    execute_table_generator()