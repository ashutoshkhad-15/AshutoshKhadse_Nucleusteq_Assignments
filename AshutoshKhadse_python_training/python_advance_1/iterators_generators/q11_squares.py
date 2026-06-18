"""
11. Write a generator function that yields square numbers up to N.
"""
from typing import Generator

# Constants
MAX_SQUARE_LIMIT: int = 4

def generate_squares(max_limit: int) -> Generator[int, None, None]:
    """Yields square numbers starting from 1 up to max_limit."""
    current_number: int = 1
    
    while current_number <= max_limit:
        # yield suspends execution, sends the value back, and waits for the next call
        yield current_number ** 2
        current_number += 1

if __name__ == "__main__":
    square_gen = generate_squares(MAX_SQUARE_LIMIT)
    for square in square_gen:
        print(square)