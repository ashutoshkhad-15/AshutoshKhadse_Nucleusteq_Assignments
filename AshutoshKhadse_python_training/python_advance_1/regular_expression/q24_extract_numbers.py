"""
24. Write a program to extract all numbers from a given string using regular expressions.
"""
import re
from typing import List

# Constants
SAMPLE_TEXT: str = "Order 123 was placed on 2023-10-25 with a total of 450 items."
NUMBER_PATTERN: str = r'\d+'

def extract_numbers(text: str) -> List[str]:
    """
    Finds and extracts all sequences of continuous digits from a string.
    """
    # re.findall returns a list of all non-overlapping matches in the string
    extracted_numbers: List[str] = re.findall(NUMBER_PATTERN, text)
    return extracted_numbers

if __name__ == "__main__":
    result: List[str] = extract_numbers(SAMPLE_TEXT)
    print(f"Original Text: {SAMPLE_TEXT}")
    print(f"Extracted Numbers: {result}")