from typing import Union

Number = Union[int, float]

def multiply(a: Number, b: Number) -> Number:
    """Returns the product of two numbers."""
    return a * b

def divide(a: Number, b: Number) -> float:
    """Returns the quotient of two numbers. Raises ValueError on zero division."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b