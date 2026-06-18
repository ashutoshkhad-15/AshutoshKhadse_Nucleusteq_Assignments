"""
19. Use filter() to extract even numbers from a list.
"""
from typing import List

# Constants
MIXED_NUMBERS: List[int] = [10, 15, 20, 25, 30]

def get_even_numbers(numbers: List[int]) -> List[int]:
    """Uses filter() to extract even numbers from a given list."""
    
    # filter() keeps only the elements for which the lambda evaluates to True
    return list(filter(lambda x: x % 2 == 0, numbers))

if __name__ == "__main__":
    evens: List[int] = get_even_numbers(MIXED_NUMBERS)
    print(f"Original sequence: {MIXED_NUMBERS}")
    print(f"Filtered even numbers: {evens}")