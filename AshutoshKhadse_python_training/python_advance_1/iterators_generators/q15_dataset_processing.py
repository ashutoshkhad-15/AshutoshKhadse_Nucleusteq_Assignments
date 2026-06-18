"""
15. Write a program that processes a large dataset using a generator instead of storing all values in a list.
"""
from typing import Generator

# Constants
TOTAL_VIRTUAL_ROWS: int = 1000000
ROWS_TO_PROCESS: int = 5

def simulate_large_file_read(total_lines: int) -> Generator[str, None, None]:
    """
    Simulates reading a massive dataset.
    Because we use 'yield', Python only stores one row in memory at a time.
    """
    line_number: int = 1
    while line_number <= total_lines:
        # Imagine this is reading a line from a 10GB CSV file
        yield f"Dataset Row Data: {line_number}"
        line_number += 1

def process_data() -> None:
    """Processes the generated data safely without memory overflow."""
    data_generator = simulate_large_file_read(TOTAL_VIRTUAL_ROWS)

    # We only process the first 5 to demonstrate the concept in the terminal
    for _ in range(ROWS_TO_PROCESS):
        current_row: str = next(data_generator)
        print(f"Processing -> {current_row}")

if __name__ == "__main__":
    process_data()