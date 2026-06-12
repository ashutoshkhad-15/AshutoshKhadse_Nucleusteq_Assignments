"""
Module   : q09_largest_of_three.py
Package  : python_basic.operators_conditionals
Topics   : Python Basics – Operators & Conditionals
Question 9 : Find the largest of three numbers.
"""

def find_largest_number(num1: float, num2: float, num3: float) -> float:
    """
    Compares three numbers and returns the largest value using standard conditional logic.
    
    Args:
        num1 : First number.
        num2 : Second number.
        num3 : Third number.

    Returns:
        The largest of the three values.
    """

    if num1 >= num2 and num1 >= num3:
        return num1
    elif num2 >= num1 and num2 >= num3:
        return num2
    else:
        return num3

def execute_largest_finder() -> None:
    """
    Takes three numbers as input and displays the largest.
    """
    
    num1: float = float(input("Enter the first number: "))
    num2: float = float(input("Enter the second number: "))
    num3: float = float(input("Enter the third number: "))
    
    largest: float = find_largest_number(num1, num2, num3)
    print(f"\nThe largest number among {num1}, {num2}, and {num3} is {largest}.")


if __name__ == "__main__":
    execute_largest_finder()