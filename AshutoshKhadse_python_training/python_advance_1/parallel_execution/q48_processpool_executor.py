"""
48. Convert a normal function into parallel execution using ProcessPoolExecutor.
"""
import math
from concurrent.futures import ProcessPoolExecutor
from typing import List

# Constants
# These numbers represent computationally heavy factorials
HEAVY_COMPUTATION_TARGETS: List[int] = [50, 60, 70, 80]
MAX_CPU_PROCESSES: int = 4

def calculate_massive_factorial(number: int) -> int:
    """
    A normal, heavily CPU-bound function.
    Calculates the factorial of a massive integer and returns the digit count.
    """
    print(f"Calculating factorial for {number}...")
    # math.factorial is optimized in C, but still takes CPU time for massive numbers
    result: int = math.factorial(number)
    
    # We return the length of the string representation instead of the full number
    # to avoid flooding the terminal with millions of digits.
    digit_count: int = len(str(result))
    return digit_count

def execute_with_process_pool(targets: List[int]) -> None:
    """Distributes heavy CPU calculations across multiple processor cores."""
    print("Starting ProcessPoolExecutor for heavy CPU calculations...\n")
    
    # The 'with' statement manages the OS-level process cleanup
    with ProcessPoolExecutor(max_workers=MAX_CPU_PROCESSES) as executor:
        # .map() chunks the input array and sends it to different CPU cores
        results = list(executor.map(calculate_massive_factorial, targets))
        
    print("\n Calculations Complete ")
    for target, length in zip(targets, results):
        print(f"The factorial of {target} has {length} digits.")

if __name__ == "__main__":
    execute_with_process_pool(HEAVY_COMPUTATION_TARGETS)