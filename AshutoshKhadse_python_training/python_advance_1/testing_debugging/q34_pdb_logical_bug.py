"""
34. Create a function with a logical bug and use pdb to identify the issue.
"""
import pdb
from typing import List

# Constants
BUGGY_LIST: List[int] = [-10, -5, -3, -20]

def find_maximum_value(numbers: List[int]) -> int:
    """
    Finds the maximum value in a list of integers.
    (Contains a deliberate logical bug for debugging practice).
    """
    if not numbers:
        raise ValueError("The list is empty.")
    
    # BUG: Initializing to 0 assumes all lists will have positive numbers.
    max_value: int = 0  
    
    # Trigger the debugger right before the problematic logic
    pdb.set_trace() 
    
    for current_number in numbers:
        if current_number > max_value:
            max_value = current_number
            
    return max_value

if __name__ == "__main__":
    print(f"Analyzing list: {BUGGY_LIST}")
    # When this runs, execution will pause. 
    # In the pdb terminal, you would type 'p max_value' to see it's 0, 
    # then type 'n' (next) to step through and realize the 'if' statement never triggers.
    result: int = find_maximum_value(BUGGY_LIST)
    print(f"The calculated maximum is: {result}")