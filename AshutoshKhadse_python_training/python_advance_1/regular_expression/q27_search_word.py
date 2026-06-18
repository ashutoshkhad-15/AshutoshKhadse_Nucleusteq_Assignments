"""
27. Use re.search() to check whether a word exists in a sentence.
"""
import re

# Constants
SENTENCE: str = "The quick brown fox jumps over the lazy dog."
TARGET_WORD: str = "fox"
MISSING_WORD: str = "cat"

def word_exists_in_sentence(sentence: str, target_word: str) -> bool:
    """
    Searches for an exact word match within a sentence using word boundaries (\b).
    """
    # \b ensures we match the whole word "fox", not a substring like in "foxy"
    # re.IGNORECASE makes the search case-insensitive
    pattern: str = rf'\b{target_word}\b'
    match = re.search(pattern, sentence, re.IGNORECASE)
    
    return bool(match)

if __name__ == "__main__":
    print(f"Sentence: '{SENTENCE}'")
    print(f"Contains '{TARGET_WORD}': {word_exists_in_sentence(SENTENCE, TARGET_WORD)}")
    print(f"Contains '{MISSING_WORD}': {word_exists_in_sentence(SENTENCE, MISSING_WORD)}")