"""
Module   : q27_manual_list_reverse.py
Package  : python_basic.data_structures
Topics   : Data Structures – List
Question 27: Reverse a list without using reverse().
"""

from typing import List, Any

def manual_reverse(elements: List[Any]) -> List[Any]:
    """
    Reverses a list in-place using a two-pointer swapping algorithm.
    """
    # Creating a shallow copy ensures the function remains "pure" and doesn't 
    # unintentionally mutate the original list variable passed into it.
    reversed_list: List[Any] = elements[:]
    
    # Initialize pointers at the extreme ends of the list
    left_index: int = 0
    right_index: int = len(reversed_list) - 1
    
    # Swap elements moving inwards until the pointers meet in the middle
    while left_index < right_index:
        # Pythonic tuple unpacking allows swapping without a temporary variable
        reversed_list[left_index], reversed_list[right_index] = reversed_list[right_index], reversed_list[left_index]
        
        left_index += 1
        right_index -= 1
        
    return reversed_list

def execute_manual_reversal() -> None:
    """
    Captures user input and executes the manual reversal algorithm.
    """
    
    user_input: str = input("Enter a sequence of items separated by commas: ")
    
    # Splitting the string creates a list of strings. We leave them as strings 
    # because reversal logic does not require numerical data types to work.
    original_list: List[str] = [item.strip() for item in user_input.split(",")]
    
    reversed_result: List[str] = manual_reverse(original_list)
    
    print(f"\nOriginal List : {original_list}")
    print(f"Reversed List : {reversed_result}")

if __name__ == "__main__":
    execute_manual_reversal()