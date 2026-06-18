"""
A utility module for string manipulation.
"""

def reverse_string(text: str) -> str:
    """Returns the reversed version of the provided string."""
    return text[::-1]

def count_vowels(text: str) -> int:
    """Counts and returns the number of vowels in a string."""
    vowels: set[str] = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for char in text.lower() if char in vowels)