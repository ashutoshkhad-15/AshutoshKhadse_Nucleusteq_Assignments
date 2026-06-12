"""
Module   : q07_even_odd_checker.py
Package  : python_basic.operators_conditionals
Topics   : Python Basics – Operators & Conditionals
Question 7 : Write a program to check whether a number is even or odd.
"""

def check_even_odd(number: int) -> str:
    """
    Evaluates whether a given integer is even or odd using the modulo operator.
    Args:
        number : The integer to check.

    Returns:
        'Even' or 'Odd'.
    """
    return "Even" if number % 2 == 0 else "Odd"


def execute_even_odd_checker() -> None:
    """
    Handles user input and displays the even/odd result.
    Assumes standard integer input.
    """
    
    user_input: int = int(input("Enter an integer: "))
    
    result: str = check_even_odd(user_input)
    print(f"The number {user_input} is {result}.")


if __name__ == "__main__":
    execute_even_odd_checker()