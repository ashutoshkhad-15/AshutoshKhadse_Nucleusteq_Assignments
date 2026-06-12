"""
Module   : q11_leap_year_checker.py
Package  : python_basic.operators_conditionals
Topics   : Python Basics – Operators & Conditionals
Question 11: Check whether a year is a leap year.
"""

def is_leap_year(year: int) -> bool:
    """
    Determines if a given year is a leap year according to the Gregorian calendar rules.
    Returns True if it is a leap year, False otherwise.
    """
    # A year is a leap year if it is divisible by 4.
    # Also, if it is a century year (divisible by 100), it is NOT a leap year,
    # UNLESS it is also divisible by 400.
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


def execute_leap_year_checker() -> None:
    """
    Captures a year from the user and prints whether it is a leap year.
    """
    
    input_year: int = int(input("Enter a year: "))
    
    if is_leap_year(input_year):
        print(f"{input_year} is a Leap Year.")
    else:
        print(f"{input_year} is NOT a Leap Year.")


if __name__ == "__main__":
    execute_leap_year_checker()