"""
28. Use re.findall() to extract all words starting with a capital letter.
"""
import re
from typing import List

# Constants
MIXED_CASE_TEXT: str = "Alice and Bob traveled to Paris during the Spring."
CAPITALIZED_WORD_PATTERN: str = r'\b[A-Z][a-z]*\b'

def extract_capitalized_words(text: str) -> List[str]:
    """
    Extracts all words from a string that begin with an uppercase letter.
    """
    # \b represents a word boundary. [A-Z] matches exactly one capital letter.
    # [a-z]* matches zero or more lowercase letters following it.
    return re.findall(CAPITALIZED_WORD_PATTERN, text)

if __name__ == "__main__":
    capital_words: List[str] = extract_capitalized_words(MIXED_CASE_TEXT)
    print(f"Original Text: {MIXED_CASE_TEXT}")
    print(f"Capitalized Words Found: {capital_words}")