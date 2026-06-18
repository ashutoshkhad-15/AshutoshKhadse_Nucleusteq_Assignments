"""
44. Create multiple threads to simulate file downloading using time.sleep().
"""
import threading
import time
from typing import List

# Constants
FILES_TO_DOWNLOAD: List[str] = ["video.mp4", "dataset.csv", "image.png"]
DOWNLOAD_DELAY_MULTIPLIER: float = 1.5

def download_file(filename: str, file_index: int) -> None:
    """
    Simulates downloading a single file. 
    The sleep duration is staggered based on the file index to simulate varying file sizes.
    """
    print(f"Started downloading: {filename}")
    
    # Simulate network delay (larger index = longer simulated download)
    simulated_time: float = (file_index + 1) * DOWNLOAD_DELAY_MULTIPLIER
    time.sleep(simulated_time)
    
    print(f"Finished downloading: {filename} (took {simulated_time}s)")

def execute_parallel_downloads(files: List[str]) -> None:
    """Creates multiple threads to download files concurrently."""
    threads: List[threading.Thread] = []
    
    # Step 1: Create and start a thread for each file
    for index, file in enumerate(files):
        thread = threading.Thread(target=download_file, args=(file, index))
        threads.append(thread)
        thread.start()
        
    # Step 2: Ensure the main program waits for ALL downloads to finish
    for thread in threads:
        thread.join()
        
    print("System Message: All parallel file downloads are complete!")

if __name__ == "__main__":
    execute_parallel_downloads(FILES_TO_DOWNLOAD)