"""
Module   : q33_character_frequency.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 33: Count frequency of characters in a string using dictionary.
"""

from typing import Dict

def count_character_frequency(text: str) -> Dict[str, int]:
    """
    Iterates through a string and builds a frequency map of its characters.
    """
    frequency_map: Dict[str, int] = {}
    
    # We iterate through each character in the string (O(n) time complexity)
    for char in text:
        # We use .get() to safely check if the character already exists in the dictionary.
        # If it doesn't, it defaults to 0, and we add 1. If it does, we increment its current value.
        frequency_map[char] = frequency_map.get(char, 0) + 1
        
    return frequency_map

def execute_frequency_counter() -> None:
    """
    Takes user string input and outputs the character frequency dictionary.
    """
    
    user_text: str = input("Enter a word or sentence to analyze: ")
    
    # Edge case handling for empty inputs
    if not user_text.strip():
        print("Error: Input cannot be empty.")
        return
        
    result_map: Dict[str, int] = count_character_frequency(user_text)
    
    for character, count in result_map.items():
        # Representing spaces cleanly in the output
        display_char = "' '" if character == " " else character
        print(f"Character {display_char:<3} : {count}")

if __name__ == "__main__":
    execute_frequency_counter()