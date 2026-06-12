"""
Module   : q18_palindrome_checker.py
Package  : python_basic.functions
Topics   : Functions
Question 18: Write a function to check palindrome (Number and string).
"""

from typing import Union

def is_palindrome(value: Union[str, int]) -> bool:
    """
    Determines if a given string or integer reads the same forwards and backwards.
    
    Args:
        value : An integer (e.g. 121) or string (e.g. 'racecar') to check.

    Returns:
        True if the value is a palindrome, False otherwise.

    """
    # Standardizing the input into a string allows the same slicing logic 
    # to be safely applied to both numerical and textual inputs.
    string_representation: str = str(value)
    return string_representation == string_representation[::-1]

def execute_palindrome_checker() -> None:
    """
    Captures user input, validates it is not empty, and checks for palindrome properties.
    """
    
    try:
        # .strip() removes accidental leading/trailing spaces that would break the palindrome logic
        user_input: str = input("Enter a word or number: ").lower().strip()
        
        # Manually raising a ValueError ensures we don't process empty strings
        if not user_input:
            raise ValueError("Input cannot be completely empty or just spaces.")
            
        if is_palindrome(user_input):
            print(f"'{user_input}' is a Palindrome.")
        else:
            print(f"'{user_input}' is NOT a Palindrome.")
            
    except ValueError as error_msg:
        print(f"Validation Error: {error_msg}")
    except Exception as generic_error:
        # A generic catch-all is a standard safeguard against unforeseen edge cases
        print(f"An unexpected system error occurred: {generic_error}")

if __name__ == "__main__":
    execute_palindrome_checker()