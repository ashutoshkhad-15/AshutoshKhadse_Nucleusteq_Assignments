"""
Module   : q25_list_operations.py
Package  : python_basic.data_structures
Topics   : Data Structures – List
Question 25: Create a list of 10 numbers and find sum, max, sort it, and remove duplicates.
"""

from typing import Any, List, Dict

def analyze_list(numbers: List[int]) -> Dict[str, Any]:
    """
    Perform a full analysis of a numeric list:
    compute the total, find the maximum, produce a sorted copy,
    and return a deduplicated version.

    Args:
        numbers : A list of integers (may contain duplicates).

    Returns:
        A dict with keys: 'sum', 'max', 'sorted', 'unique'.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot analyse an empty list.")

    return {
        "sum": sum(numbers),
        "max": max(numbers),
        "sorted": sorted(numbers),
        # set() collapses duplicates; sorted() gives a deterministic order
        "unique": sorted(set(numbers)),
    }


def execute_list_operations() -> None:
    """
    Generates a predefined list of 10 numbers (with intentional duplicates to prove 
    the removal logic) and processes it.
    """
    
    # Intentionally inserting duplicates to demonstrate the set() logic
    sample_list: List[int] = [42, 15, 8, 99, 15, 23, 42, 4, 16, 8]
    print(f"Original List (10 items) : {sample_list}")
    
    try:
        results = analyze_list(sample_list)
        
        print("\n Analysis Results ")
        for operation, result in results.items():
            print(f"{operation:<16}: {result}")
            
    except ValueError as error_msg:
        print(f"Error: {error_msg}")


if __name__ == "__main__":
    execute_list_operations()