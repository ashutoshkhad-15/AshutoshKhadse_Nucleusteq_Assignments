"""
40. Create a package for mathematical operations (add, subtract, multiply, divide) and use it.
"""
# Because of __init__.py, we don't have to import from basic_math or advanced_math explicitly.
from math_ops import add, subtract, multiply, divide

# Constants
VALUE_X: float = 15.0
VALUE_Y: float = 3.0

def run_calculations() -> None:
    """Uses the math_ops package to perform arithmetic operations."""
    print(f"Addition: {VALUE_X} + {VALUE_Y} = {add(VALUE_X, VALUE_Y)}")
    print(f"Subtraction: {VALUE_X} - {VALUE_Y} = {subtract(VALUE_X, VALUE_Y)}")
    print(f"Multiplication: {VALUE_X} * {VALUE_Y} = {multiply(VALUE_X, VALUE_Y)}")
    
    try:
        print(f"Division: {VALUE_X} / {VALUE_Y} = {divide(VALUE_X, VALUE_Y)}")
    except ValueError as e:
        print(f"Division Error: {e}")

if __name__ == "__main__":
    run_calculations()