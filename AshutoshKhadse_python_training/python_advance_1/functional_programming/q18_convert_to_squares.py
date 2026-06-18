"""
18. Use map() to convert a list of numbers into their squares.
"""
from typing import List

# Constants
INPUT_NUMBERS: List[int] = [1, 2, 3, 4, 5]

def get_squares_with_map(numbers: List[int]) -> List[int]:
    """Uses map() to convert a list of numbers into their squares."""
    
    # map() applies the lambda function to each element in the iterable
    # We cast it back to a list to view the results immediately
    return list(map(lambda x: x ** 2, numbers))

if __name__ == "__main__":
    squared_numbers: List[int] = get_squares_with_map(INPUT_NUMBERS)
    print(f"Original sequence: {INPUT_NUMBERS}")
    print(f"Squared sequence: {squared_numbers}")