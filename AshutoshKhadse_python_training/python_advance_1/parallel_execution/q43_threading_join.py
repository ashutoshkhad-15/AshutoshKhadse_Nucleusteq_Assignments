"""
43. Demonstrate the use of join() method in threading.
"""
import threading
import time

# Constants
WORKER_DELAY: float = 2.0

def long_running_task() -> None:
    """Simulates a heavy background task."""
    print("Worker Thread: Starting heavy processing...")
    time.sleep(WORKER_DELAY)
    print("Worker Thread: Processing finished!")

def demonstrate_join() -> None:
    """
    Demonstrates how join() blocks the main thread until 
    the target thread completes its execution.
    """
    worker_thread = threading.Thread(target=long_running_task)
    
    print("Main Thread: Starting the worker thread.")
    worker_thread.start()
    
    print("Main Thread: Waiting for the worker thread to finish using join()...")
    
    # join() forces the Main Thread to pause right here.
    # Without this line, the Main Thread would print the exit message immediately.
    worker_thread.join()
    
    print("Main Thread: Worker has joined. Main program exiting safely.")

if __name__ == "__main__":
    demonstrate_join()