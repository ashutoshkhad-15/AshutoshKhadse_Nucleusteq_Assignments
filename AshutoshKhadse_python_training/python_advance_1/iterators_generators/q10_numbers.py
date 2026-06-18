"""
10. Write a custom iterator class that returns numbers from 1 to N.
"""
# Constants
TARGET_NUMBER: int = 5

class NumberIterator:
    """A custom iterator class that returns numbers from 1 to N."""

    def __init__(self, max_value: int) -> None:
        """Initializes the iterator with a maximum target value."""
        self.max_value: int = max_value
        self.current_value: int = 1

    def __iter__(self) -> 'NumberIterator':
        """Returns the iterator object itself. Required for an object to be an iterator."""
        return self

    def __next__(self) -> int:
        """Returns the next number in the sequence or raises StopIteration when done."""
        if self.current_value > self.max_value:
            # Signals that the iteration is complete
            raise StopIteration
        
        # Store the current value to return, then increment the internal counter
        value_to_return: int = self.current_value
        self.current_value += 1
        
        return value_to_return

if __name__ == "__main__":
    number_iter = NumberIterator(TARGET_NUMBER)
    for number in number_iter:
        print(number)