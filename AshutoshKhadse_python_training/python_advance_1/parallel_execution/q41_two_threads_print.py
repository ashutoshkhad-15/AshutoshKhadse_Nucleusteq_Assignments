"""
41. Write a program to create two threads that print numbers from 1 to 5 simultaneously.
"""
import threading
import time

# Constants
MAX_NUMBER: int = 5
SLEEP_INTERVAL: float = 0.3

def print_numbers(thread_name: str) -> None:
    """Prints numbers from 1 to MAX_NUMBER, simulating work with a sleep interval."""
    for i in range(1, MAX_NUMBER + 1):
        print(f"[{thread_name}] prints: {i}")
        # Sleep to allow context switching between the threads
        time.sleep(SLEEP_INTERVAL)

def execute_concurrent_printing() -> None:
    """Creates and runs two threads simultaneously."""
    # Initialize threads pointing to the target function
    thread_a = threading.Thread(target=print_numbers, args=("Thread-A",))
    thread_b = threading.Thread(target=print_numbers, args=("Thread-B",))

    # Start execution of both threads
    thread_a.start()
    thread_b.start()

    # Ensure main thread waits for both to finish before exiting
    thread_a.join()
    thread_b.join()
    
    print("Both threads have finished executing.")

if __name__ == "__main__":
    execute_concurrent_printing()