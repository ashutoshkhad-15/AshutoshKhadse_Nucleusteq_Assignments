"""
Module   : q29_tuple_to_list.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 29: Convert tuple into list and modify it.
"""

from typing import Tuple, List, Any

def convert_and_modify(original_tuple: Tuple[Any, ...]) -> List[Any]:
    """
    Converts an immutable tuple into a mutable list and applies modifications.
    """
    # Step 1: Convert tuple to list
    converted_list: List[Any] = list(original_tuple)
    
    # Step 2: Modify the new list
    converted_list.append("New Element")
    if converted_list:
        converted_list[0] = "Modified First Element"
        
    return converted_list

def execute_conversion() -> None:
    """
    Executes the conversion logic and displays the resulting state and data types.
    """
    print(" Tuple to List Conversion ")
    
    starting_tuple: Tuple[str, str, str] = ("Apple", "Banana", "Cherry")
    print(f"Original Data : {starting_tuple} | Type: {type(starting_tuple)}")
    
    modified_list: List[Any] = convert_and_modify(starting_tuple)
    
    print(f"Modified Data : {modified_list} | Type: {type(modified_list)}")

if __name__ == "__main__":
    execute_conversion()