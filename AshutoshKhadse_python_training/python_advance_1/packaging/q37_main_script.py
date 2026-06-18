"""
37. Create a module with two utility functions and import it into another Python file.
"""
from q37_string_utils import reverse_string, count_vowels

# Constants
SAMPLE_TEXT: str = "Python Packaging is Awesome"

def run_utilities() -> None:
    """Demonstrates importing and using functions from an external module."""
    reversed_text: str = reverse_string(SAMPLE_TEXT)
    vowel_count: int = count_vowels(SAMPLE_TEXT)
    
    print(f"Original: {SAMPLE_TEXT}")
    print(f"Reversed: {reversed_text}")
    print(f"Vowel Count: {vowel_count}")

if __name__ == "__main__":
    run_utilities()