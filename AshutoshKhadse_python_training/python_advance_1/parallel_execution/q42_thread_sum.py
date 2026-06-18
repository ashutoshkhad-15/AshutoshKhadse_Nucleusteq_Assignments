"""
42. Create a thread that calculates the sum of numbers from 1 to 100.
"""
import threading

# Constants
TARGET_LIMIT: int = 100

class SumCalculatorThread(threading.Thread):
    """
    A custom thread class that calculates the sum of numbers 
    from 1 to a specified limit using Object-Oriented Principles.
    """
    def __init__(self, limit: int) -> None:
        super().__init__()
        self.limit: int = limit
        self.result: int = 0

    def run(self) -> None:
        """The core logic executed automatically when the thread starts."""
        # Using Python's built-in sum() for efficiency
        self.result = sum(range(1, self.limit + 1))
        print(f"Thread Calculation Complete. Sum of 1 to {self.limit} is: {self.result}")

def execute_sum_thread() -> None:
    """Instantiates and starts the custom calculator thread."""
    calc_thread = SumCalculatorThread(TARGET_LIMIT)
    
    # .start() internally calls the .run() method defined in the class
    calc_thread.start()
    calc_thread.join()

if __name__ == "__main__":
    execute_sum_thread()