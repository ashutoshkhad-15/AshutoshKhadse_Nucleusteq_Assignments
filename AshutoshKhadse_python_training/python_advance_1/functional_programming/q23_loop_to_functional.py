"""
23. Convert a simple  loop-based program into a functional style using map or filter.
"""
from typing import List, Iterator

# Constants
DATA_STREAM: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def process_imperative(data: List[int]) -> List[int]:
    """
    Traditional loop-based approach.
    Goal: Filter for even numbers and double them.
    """
    results: List[int] = []
    for num in data:
        if num % 2 == 0:
            results.append(num * 2)
    return results

def process_functional(data: List[int]) -> List[int]:
    """
    Functional approach using filter() and map().
    Goal: Filter for even numbers and double them without using loops.
    """
    # 1. Filter out odd numbers
    even_numbers: Iterator[int] = filter(lambda x: x % 2 == 0, data)
    
    # 2. Map the remaining even numbers by multiplying by 2
    doubled_numbers: Iterator[int] = map(lambda x: x * 2, even_numbers)
    
    return list(doubled_numbers)

if __name__ == "__main__":
    print(f"Original Data Sequence: {DATA_STREAM}")
    
    # Both approaches will yield the exact same result
    imperative_result: List[int] = process_imperative(DATA_STREAM)
    print(f"Imperative Approach Result: {imperative_result}")
    
    functional_result: List[int] = process_functional(DATA_STREAM)
    print(f"Functional Approach Result: {functional_result}")