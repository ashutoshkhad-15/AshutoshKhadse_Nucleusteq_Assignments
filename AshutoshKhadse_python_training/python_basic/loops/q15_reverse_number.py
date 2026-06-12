"""
Module   : q15_reverse_number.py
Package  : python_basic.loops
Topics   : Python Basics – Loops
Question 15: Reverse a number using loop.
"""

def reverse_integer(number: int) -> int:
    """
    Reverses the digits of an integer using a mathematical while loop.
    """
    # We extract the sign to handle negative numbers gracefully, 
    # ensuring the mathematical logic only deals with absolute values.
    is_negative: bool = number < 0
    number = abs(number)
    
    reversed_num: int = 0
    
    while number > 0:
        last_digit: int = number % 10
        reversed_num = (reversed_num * 10) + last_digit
        number = number // 10  # Floor division removes the last digit
        
    # Reapply the negative sign if the original number was negative
    return -reversed_num if is_negative else reversed_num


def execute_reversal() -> None:
    """
    Takes an integer input from the user and outputs the reversed value.
    """
    val: int = int(input("Enter an integer to reverse: "))
    
    reversed_val: int = reverse_integer(val)
    print(f"Original: {val} | Reversed: {reversed_val}")


if __name__ == "__main__":
    execute_reversal()