"""
Module   : q05_swap_numbers.py
Package  : python_basic.variables_datatypes
Topics   : Python Basics – Variables & Data Types
Question 5 : Write a program to swap two numbers.
"""

from typing import Tuple

def swap_numbers(first: float, second: float) -> Tuple[float, float]:
    """
    Swap two numbers using Python's tuple unpacking (no temporary variable).

    The right-hand side creates a tuple (second, first) before any assignment
    happens, so both values are captured simultaneously.

    Args:
        first  : The first number.
        second : The second number.

    Returns:
        A tuple (second, first) : the two values swapped.
    """
    first, second = second, first
    return first, second

if __name__ == "__main__":
    num1: float = 11
    num2: float = 20
    print(f"Before swapping: num1 = {num1}, num2 = {num2}")
    num1, num2 = swap_numbers(num1, num2)
    print(f"After swapping:  num1 = {num1}, num2 = {num2}")