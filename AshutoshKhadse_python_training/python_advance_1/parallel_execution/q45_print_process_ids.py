"""
45. Write a program to create two processes that print their Process IDs.
"""
import multiprocessing
import os
import time

# Constants
PROCESS_NAME_A: str = "Worker-Process-A"
PROCESS_NAME_B: str = "Worker-Process-B"
DELAY: float = 0.5

def display_process_info(process_alias: str) -> None:
    """
    Retrieves and prints the Process ID (PID) for the currently running process.
    """
    # os.getpid() asks the operating system for the current process identifier
    current_pid: int = os.getpid()
    print(f"[{process_alias}] is running on Process ID: {current_pid}")
    
    # Adding a slight delay to ensure output interleaving is readable
    time.sleep(DELAY)

def execute_multiprocessing() -> None:
    """Creates and executes two parallel OS-level processes."""
    main_pid: int = os.getpid()
    print(f"Main Program is starting on Process ID: {main_pid}\n")

    # Initialize the Process objects targeting our function
    process_1 = multiprocessing.Process(target=display_process_info, args=(PROCESS_NAME_A,))
    process_2 = multiprocessing.Process(target=display_process_info, args=(PROCESS_NAME_B,))

    # Start the processes (spawns new Python interpreters in the background)
    process_1.start()
    process_2.start()

    # Wait for both processes to complete before exiting
    process_1.join()
    process_2.join()
    
    print("\nBoth parallel processes have finished execution.")

if __name__ == "__main__":
    execute_multiprocessing()