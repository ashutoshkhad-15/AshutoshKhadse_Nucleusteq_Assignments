"""
16. Show an example of a built-in generator (like range) and iterate over it.
"""
from typing import Iterable

# Constants
RANGE_START: int = 1
RANGE_END: int = 6

def demonstrate_built_in_generator(start: int, end: int) -> None:
    """Demonstrates how the built-in range() acts as a lazy iterable generator."""
    
    # range() is a built-in sequence type that behaves like a generator.
    # It does not construct an entire list in memory; it yields numbers on the fly.
    range_sequence: Iterable[int] = range(start, end)
    
    print(f"Data type of the range object: {type(range_sequence)}")
    
    # Iterating over the sequence element by element
    for number in range_sequence:
        print(f"Generated number: {number}")

if __name__ == "__main__":
    demonstrate_built_in_generator(RANGE_START, RANGE_END)