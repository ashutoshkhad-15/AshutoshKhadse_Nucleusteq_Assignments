"""
Module   : q31_remove_duplicates_set.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 31: Remove duplicates from list using set.
"""

from typing import Any, List, Set

def remove_duplicates_preserving_order(items: List[Any]) -> List[Any]:
    """
    Remove duplicates from a list while preserving the original insertion order.

    Why not just use set()?
        set() does remove duplicates, but it destroys order.
        This function uses a 'seen' set for O(1) lookup while rebuilding the
        list in its original sequence — O(n) overall.

    Args:
        items : A list that may contain duplicate values.

    Returns:
        A new list with duplicates removed, in their first-seen order.
    """
    seen: Set[Any] = set()
    unique_items: List[Any] = []

    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items

def execute_deduplication() -> None:
    """
    Captures a list of numbers with duplicates from the user and cleans it.
    """
    print(" List Deduplication via Sets ")
    
    try:
        user_input: str = input("Enter numbers with duplicates separated by commas: ")
        raw_list: List[int] = [int(num.strip()) for num in user_input.split(",")]
        
        cleaned_list: List[int] = remove_duplicates_preserving_order(raw_list)
        
        print(f"\nOriginal List (with duplicates) : {raw_list}")
        print(f"Cleaned List (unique elements)  : {cleaned_list}")
        
    except ValueError:
        print("Error: Please enter only integer numbers separated by commas.")

if __name__ == "__main__":
    execute_deduplication()