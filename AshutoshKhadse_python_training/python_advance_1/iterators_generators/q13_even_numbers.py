"""
13. Write a generator expression to generate even numbers from 1 to 50.
"""
from typing import Generator

# Constants
START_NUM: int = 1
END_NUM: int = 50

def get_even_numbers_generator(start: int, end: int) -> Generator[int, None, None]:
    """Returns a generator expression for even numbers within a range."""
    # A generator expression uses parentheses () instead of list brackets []
    # This evaluates lazily instead of loading all 50 numbers into memory at once
    return (num for num in range(start, end + 1) if num % 2 == 0)

if __name__ == "__main__":
    even_gen = get_even_numbers_generator(START_NUM, END_NUM)
    for even_num in even_gen:
        print(even_num, end=" ")