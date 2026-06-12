"""
Module   : q12_print_numbers.py
Package  : python_basic.loops
Topics   : Python Basics – Loops
Question 12: Print numbers from 1 to 100 using loop.
"""

def print_numbers_one_to_hundred() -> None:
    """
    Print all integers from 1 to 100 (inclusive) on a single line,
    separated by spaces.
    """
    for number in range(1, 101):
        # end=" " keeps all numbers on one line; the final print adds a newline
        print(number, end=" ")
    print()  # newline after the last number

if __name__ == "__main__":
    print_numbers_one_to_hundred()