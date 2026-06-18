"""
12. Write a generator to produce Fibonacci numbers.
"""
from typing import Generator

# Constants
FIBONACCI_LIMIT: int = 8

def generate_fibonacci(limit: int) -> Generator[int, None, None]:
    """Generates Fibonacci numbers up to a specified count limit."""
    num_a: int = 0
    num_b: int = 1
    count: int = 0

    while count < limit:
        yield num_a
        # Simultaneously update values for the next iteration (a becomes b, b becomes a+b)
        num_a, num_b = num_b, num_a + num_b
        count += 1

if __name__ == "__main__":
    fib_gen = generate_fibonacci(FIBONACCI_LIMIT)
    for num in fib_gen:
        print(num)