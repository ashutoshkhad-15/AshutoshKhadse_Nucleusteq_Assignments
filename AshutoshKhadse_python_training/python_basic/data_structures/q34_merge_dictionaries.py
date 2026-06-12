"""
Module   : q34_merge_dictionaries.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 34: Merge two dictionaries.
"""

from typing import Dict, Any

def merge_dictionaries(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Demonstrates merging two dictionaries using Python's modern unpacking operators.
    """
    # The double asterisk (**) unpacks the key-value pairs of the dictionaries.
    # If there are duplicate keys, the values from the dictionary on the right (dict2)
    # will overwrite the values from the dictionary on the left (dict1).
    # Note: In Python 3.9+, this can also be written simply as `dict1 | dict2`.
    merged_dict: Dict[str, Any] = {**dict1, **dict2}
    
    return merged_dict

def execute_dict_merge() -> None:
    """
    Provides predefined dictionaries to visually demonstrate how merging handles duplicate keys.
    """
    
    # 'department' exists in both. Admin dict will overwrite the basic employee dict.
    employee_basic: Dict[str, Any] = {"id": 101, "name": "Ashutosh", "department": "General"}
    employee_admin: Dict[str, Any] = {"department": "Engineering", "access_level": "Root"}
    
    print(f"Dictionary 1: {employee_basic}")
    print(f"Dictionary 2: {employee_admin}\n")
    
    final_merged_data: Dict[str, Any] = merge_dictionaries(employee_basic, employee_admin)
    
    print(f"Merged Result: {final_merged_data}")

if __name__ == "__main__":
    execute_dict_merge()