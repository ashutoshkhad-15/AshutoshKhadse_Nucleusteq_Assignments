"""
29. Replace multiple spaces in a string with a single space using re.sub().
"""
import re

# Constants
MESSY_STRING: str = "This    string   has     way too   many  spaces."
MULTIPLE_SPACE_PATTERN: str = r'\s+'
SINGLE_SPACE_REPLACEMENT: str = " "

def normalize_spaces(text: str) -> str:
    """
    Finds instances of one or more whitespace characters and replaces 
    them with a single space.
    """
    # \s+ matches 1 or more occurrences of whitespace (spaces, tabs, newlines)
    clean_text: str = re.sub(MULTIPLE_SPACE_PATTERN, SINGLE_SPACE_REPLACEMENT, text)
    
    # .strip() removes any trailing/leading spaces that might remain at the edges
    return clean_text.strip()

if __name__ == "__main__":
    cleaned_string: str = normalize_spaces(MESSY_STRING)
    print(f"Original: '{MESSY_STRING}'")
    print(f"Cleaned:  '{cleaned_string}'")