from typing import Union

# Type alias for cleaner code
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """Returns the sum of two numbers."""
    return a + b

def subtract(a: Number, b: Number) -> Number:
    """Returns the difference of two numbers."""
    return a - b