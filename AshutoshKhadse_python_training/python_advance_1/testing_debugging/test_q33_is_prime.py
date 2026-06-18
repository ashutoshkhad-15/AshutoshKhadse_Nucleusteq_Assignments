"""
33. Write pytest test cases for a function that checks whether a number is prime.
"""
import pytest
import math

# Application Logic 

def is_prime(number: int) -> bool:
    """
    Determines whether a given integer is a prime number.
    Returns True if prime, False otherwise.
    """
    # Numbers less than 2 are not prime by definition
    if number <= 1:
        return False
    
    # 2 is the only even prime number
    if number == 2:
        return True
    
    # Eliminate even numbers early to optimize the loop
    if number % 2 == 0:
        return False
        
    # Check for factors up to the square root of the number
    max_divisor: int = math.isqrt(number) + 1
    for i in range(3, max_divisor, 2):
        if number % i == 0:
            return False
            
    return True

# Pytest Test Cases 

@pytest.mark.parametrize("test_input, expected", [
    (2, True),      # Smallest prime
    (3, True),      # Smallest odd prime
    (17, True),     # Typical prime
    (97, True),     # Larger prime
    (1, False),     # 1 is not prime
    (0, False),     # 0 is not prime
    (-5, False),    # Negative numbers are not prime
    (4, False),     # Even non-prime
    (15, False),    # Odd non-prime
])
def test_is_prime(test_input: int, expected: bool) -> None:
    """Tests the is_prime function with known primes, non-primes, and edge cases."""
    assert is_prime(test_input) == expected