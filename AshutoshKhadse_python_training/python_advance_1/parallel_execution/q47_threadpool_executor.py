"""
47. Convert a normal function into parallel execution using ThreadPoolExecutor.
"""
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

# Constants
SIMULATED_URLS: List[str] = [
    "http://api.data.com/v1",
    "http://api.data.com/v2",
    "http://api.data.com/v3",
    "http://api.data.com/v4"
]
MAX_WORKER_THREADS: int = 3
NETWORK_DELAY: float = 1.0

def fetch_mock_data(url: str) -> str:
    """A normal, I/O-bound function simulating a network request."""
    print(f"Requesting data from {url}...")
    time.sleep(NETWORK_DELAY)  # Simulating network latency
    return f"Success: Data retrieved from {url}"

def execute_with_thread_pool(urls: List[str]) -> None:
    """Converts the normal fetch function into parallel execution."""
    print("Starting ThreadPoolExecutor...\n")
    
    # The 'with' statement automatically handles joining/cleanup of threads
    with ThreadPoolExecutor(max_workers=MAX_WORKER_THREADS) as executor:
        # .map() automatically assigns the URLs to available threads in the pool
        # It returns the results in the exact same order as the input list
        results = list(executor.map(fetch_mock_data, urls))
        
    print("\n All Network Requests Completed ")
    for res in results:
        print(res)

if __name__ == "__main__":
    execute_with_thread_pool(SIMULATED_URLS)