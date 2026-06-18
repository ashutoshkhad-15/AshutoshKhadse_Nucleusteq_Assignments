"""
9. Create an iterator for a list and print elements using next().
"""
from typing import List, Any, Iterator

# Constants
SAMPLE_LIST: List[int] = [10, 20, 30]

def print_with_iterator(data: List[Any]) -> None:
    """Creates an iterator from a list and prints elements using next()."""
    # iter() creates an iterator object from the iterable list
    list_iterator: Iterator[Any] = iter(data)
    
    try:
        # next() retrieves the next item from the iterator
        print(next(list_iterator))  # Prints 10
        print(next(list_iterator))  # Prints 20
        print(next(list_iterator))  # Prints 30
        
        # If we called next() again here, it would raise StopIteration
    except StopIteration:
        print("Reached the end of the iterator.")

if __name__ == "__main__":
    print_with_iterator(SAMPLE_LIST)