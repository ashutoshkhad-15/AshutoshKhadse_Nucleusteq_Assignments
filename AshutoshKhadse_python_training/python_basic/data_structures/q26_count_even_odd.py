"""
Module   : q26_count_even_odd.py
Package  : python_basic.data_structures
Topics   : Data Structures – List
Question 26: Count even and odd numbers in a list.
"""

from typing import List, Dict

def count_even_and_odd(numbers: List[int]) -> Dict[str, int]:
    """
    Iterates through a list of integers and counts the occurrences of even and odd numbers.
    """
    even_count: int = 0
    odd_count: int = 0
    
    # Time complexity is O(n) as we must check every element in the list exactly once.
    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
            
    return {"Even": even_count, "Odd": odd_count}

def execute_even_odd_counter() -> None:
    """
    Captures a list of integers from the user and outputs the even/odd counts.
    """
    
    try:
        user_input: str = input("Enter a list of integers separated by commas: ")
        
        # Validating and parsing the user input into a strictly integer list
        parsed_list: List[int] = [int(item.strip()) for item in user_input.split(",")]
        
        counts: Dict[str, int] = count_even_and_odd(parsed_list)
        
        print(f"\nAnalyzed List: {parsed_list}")
        print(f"Total Even Numbers: {counts['Even']}")
        print(f"Total Odd Numbers : {counts['Odd']}")
        
    except ValueError:
        print("Input Error: Please ensure you only enter whole numbers (integers) separated by commas.")

if __name__ == "__main__":
    execute_even_odd_counter()