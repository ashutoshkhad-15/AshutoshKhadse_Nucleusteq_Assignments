"""
46. Write a multiprocessing program to calculate the square of numbers using Process class.
"""
import multiprocessing
import os
from typing import List

# Constants
NUMBERS_TO_SQUARE: List[int] = [4, 7, 12, 15]

class SquareCalculatorProcess(multiprocessing.Process):
    """
    A custom process class that calculates the square of a given number.
    Subclassing allows us to encapsulate the data and execution logic.
    """
    def __init__(self, number: int) -> None:
        # Must initialize the parent class
        super().__init__()
        self.number: int = number

    def run(self) -> None:
        """The core logic executed when process.start() is called."""
        result: int = self.number ** 2
        pid: int = os.getpid()
        print(f"[PID {pid}] The square of {self.number} is {result}")

def process_number_squares(numbers: List[int]) -> None:
    """Instantiates a new process for each number in the list and runs them."""
    active_processes: List[SquareCalculatorProcess] = []

    # Step 1: Create and start a process for each number
    for num in numbers:
        proc = SquareCalculatorProcess(num)
        active_processes.append(proc)
        proc.start()

    # Step 2: Ensure the main program waits for all processes to finish
    for proc in active_processes:
        proc.join()

if __name__ == "__main__":
    print(f"Calculating squares for: {NUMBERS_TO_SQUARE}\n")
    process_number_squares(NUMBERS_TO_SQUARE)