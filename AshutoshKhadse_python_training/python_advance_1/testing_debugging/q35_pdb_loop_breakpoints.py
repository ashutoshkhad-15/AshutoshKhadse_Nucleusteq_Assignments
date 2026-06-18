"""
35. Use pdb breakpoints inside a loop and inspect variable values.
"""
import pdb
from typing import List

# Constants
MULTIPLIERS: List[int] = [1, 2, 3, 4]

def calculate_cumulative_product(numbers: List[int]) -> List[int]:
    """
    Calculates the cumulative product of a list of numbers.
    Uses a debugger inside the loop to track variable states.
    """
    running_product: int = 1
    results: List[int] = []
    
    for index, num in enumerate(numbers):
        # The built-in breakpoint() function is the modern Python 3.7+ equivalent 
        # to import pdb; pdb.set_trace(). It pauses execution on EVERY loop iteration.
        breakpoint()
        
        running_product *= num
        results.append(running_product)
        
        # DEBUGGING COMMANDS:
        # 1. Type 'p index' to see the current loop iteration.
        # 2. Type 'p num' to see the current item being processed.
        # 3. Type 'p running_product' to see the math result.
        # 4. Type 'c' (continue) to move to the next breakpoint iteration.
        
    return results

if __name__ == "__main__":
    print("Starting cumulative product calculation...")
    final_result: List[int] = calculate_cumulative_product(MULTIPLIERS)
    print(f"Final Result: {final_result}")