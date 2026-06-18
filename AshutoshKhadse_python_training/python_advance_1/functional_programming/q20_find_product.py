"""
20. Use reduce() to find the product of all elements in a list.
"""
from typing import List
from functools import reduce

# Constants
FACTORS: List[int] = [2, 3, 4, 5]

def calculate_product(numbers: List[int]) -> int:
    """Uses reduce() to find the combined product of all elements in a list."""
    
    # reduce() cumulatively applies the lambda to the items of the sequence, 
    # reducing it to a single value (e.g., (((2*3)*4)*5))
    return reduce(lambda x, y: x * y, numbers)

if __name__ == "__main__":
    total_product: int = calculate_product(FACTORS)
    print(f"The cumulative product of {FACTORS} is {total_product}.")