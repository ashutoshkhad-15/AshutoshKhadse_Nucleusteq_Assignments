"""
Module   : q19_list_maximum.py
Package  : python_basic.functions
Topics   : Functions
Question 19: Write a function that returns maximum number from a list.
"""

from typing import List

def find_maximum(numbers: List[float]) -> float:
    """
    Iterates through a list of numbers to find and return the largest value.
    
    Args:
        numbers : A non-empty list of numeric values.

    Returns:
        The maximum value, or None if the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot find the maximum value of an empty list.")
        
    current_max: float = numbers[0]
    for num in numbers[1:]:
        if num > current_max:
            current_max = num  # update current_max whenever a larger value is found
            
    return current_max

def execute_maximum_finder() -> None:
    """
    Safely captures a comma-separated list from the user, parses it into floats,
    and calculates the maximum value.
    """
    
    try:
        input_string: str = input("Enter a list of numbers separated by commas (e.g., 10, 5.5, 20): ")
        
        # A list comprehension maps the split strings into floats.
        # If the user typed a letter (e.g., '10, a, 5'), this line will automatically 
        # trigger a ValueError, which our except block will gracefully catch.
        parsed_list: List[float] = [float(item.strip()) for item in input_string.split(",")]
        
        maximum_value: float = find_maximum(parsed_list)
        print(f"\nAnalyzed List: {parsed_list}")
        print(f"The maximum value is: {maximum_value}")
        
    except ValueError:
        print("Error: Failed to parse the list. Please ensure you only enter numbers separated by commas.")

if __name__ == "__main__":
    execute_maximum_finder()