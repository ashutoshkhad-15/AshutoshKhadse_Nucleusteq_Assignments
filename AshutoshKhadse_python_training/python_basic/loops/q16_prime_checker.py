"""
Module   : q16_prime_checker.py
Package  : python_basic.loops
Topics   : Python Basics – Loops
Question 16: Check whether a number is prime.
"""

def is_prime(number: int) -> bool:
    """
    Determines if a given integer is a prime number.
    Returns True if prime, False otherwise.
    """
    # Prime numbers are strictly greater than 1
    if number <= 1:
        return False
        
    # Optimization: We only need to check for factors up to the square root 
    # of the number. This drastically reduces time complexity from O(n) to O(sqrt(n)).
    # If a number is divisible by a number larger than its square root, the corresponding 
    # factor must be smaller than the square root, which we would have already checked.
    upper_limit: int = int(number ** 0.5) + 1
    
    for i in range(2, upper_limit):
        if number % i == 0:
            return False  # If evenly divisible, it is not prime
            
    return True


def execute_prime_checker() -> None:
    """
    Takes an integer input and displays whether it is prime.
    """
    val: int = int(input("Enter an integer: "))
    
    if is_prime(val):
        print(f"{val} is a Prime Number.")
    else:
        print(f"{val} is NOT a Prime Number.")


if __name__ == "__main__":
    execute_prime_checker()