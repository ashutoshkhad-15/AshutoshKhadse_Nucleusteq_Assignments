"""
32. Write pytest test cases for a function that adds two numbers.
"""
import pytest
from typing import Union

# Application Logic 

def add_numbers(num_a: Union[int, float], num_b: Union[int, float]) -> Union[int, float]:
    """Adds two numbers and returns the result."""
    return num_a + num_b

# Pytest Test Cases 

# We use pytest.mark.parametrize to run the same test logic with multiple data sets.
# This avoids writing repetitive test functions for every single scenario.
@pytest.mark.parametrize("input_a, input_b, expected_result", [
    (5, 3, 8),            # Test positive integers
    (-2, -4, -6),         # Test negative integers
    (-5, 10, 5),          # Test mixed sign integers
    (0, 0, 0),            # Test zeros
    (2.5, 3.1, 5.6),      # Test floating point numbers
])
def test_add_numbers(input_a: Union[int, float], input_b: Union[int, float], expected_result: Union[int, float]) -> None:
    """
    Tests the add_numbers function against various valid numerical inputs.
    """
    # Arrange & Act
    actual_result: Union[int, float] = add_numbers(input_a, input_b)
    
    # Assert
    # For floats, we use pytest.approx to handle minor floating-point precision issues
    if isinstance(expected_result, float):
        assert actual_result == pytest.approx(expected_result)
    else:
        assert actual_result == expected_result

def test_add_numbers_type_error() -> None:
    """Tests that adding unsupported types (like strings) raises a TypeError."""
    with pytest.raises(TypeError):
        add_numbers("5", 3)  # type: ignore