"""
39. Create a package with two modules and include an __init__.py file..
"""
# Importing directly from the package level thanks to __init__.py
from data_tools import capitalize_words, is_non_empty

# Constants
TEST_INPUT: str = "hello world of packaging"

def process_data() -> None:
    if is_non_empty(TEST_INPUT):
        formatted_output: str = capitalize_words(TEST_INPUT)
        print(f"Processed Output: {formatted_output}")
    else:
        print("Data is empty.")

if __name__ == "__main__":
    process_data()