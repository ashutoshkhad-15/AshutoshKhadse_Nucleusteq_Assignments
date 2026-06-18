"""
30. Write a pattern to check if a string contains only alphabets.
"""
import re

# Constants
ALPHABET_PATTERN: str = r'^[a-zA-Z]+$'
TEST_STRINGS: list[str] = ["HelloWorld", "Hello World", "Python3", "abcXYZ"]

def is_only_alphabets(text: str) -> bool:
    """
    Validates that a string contains absolutely no spaces, numbers, or 
    special characters—only alphabetical characters a-z and A-Z.
    """
    # ^ ensures we start at the beginning, $ ensures we check to the end.
    return bool(re.fullmatch(ALPHABET_PATTERN, text))

if __name__ == "__main__":
    for string in TEST_STRINGS:
        validity: str = "Valid" if is_only_alphabets(string) else "Invalid"
        print(f"[{validity}] '{string}'")