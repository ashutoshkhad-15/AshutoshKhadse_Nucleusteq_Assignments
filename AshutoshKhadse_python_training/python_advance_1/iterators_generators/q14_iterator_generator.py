"""
14. Explain the difference between iterator and generator with a small example.

    Note: Please refer the attached pdf in the Assignment submission sheet for the Theory part of this question.
"""
from typing import Generator

# ITERATOR EXAMPLE 
class SimpleIterator:
    """Class-based Iterator (more verbose)."""
    def __init__(self) -> None:
        self.count: int = 0
        
    def __iter__(self) -> 'SimpleIterator':
        return self
        
    def __next__(self) -> int:
        if self.count >= 3:
            raise StopIteration
        self.count += 1
        return self.count

# GENERATOR EXAMPLE 
def simple_generator() -> Generator[int, None, None]:
    """Function-based Generator (cleaner)."""
    yield 1
    yield 2
    yield 3

if __name__ == "__main__":
    print("Iterator Output:", list(SimpleIterator()))
    print("Generator Output:", list(simple_generator()))