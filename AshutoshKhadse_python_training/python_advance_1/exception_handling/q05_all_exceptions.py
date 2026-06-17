"""
5. Write a program that catches all exceptions and prints the error message.
"""
# Constants
INDEX_TO_ACCESS: int = 10
SAMPLE_LIST: list[int] = [1, 2, 3]

def risky_operation() -> None:
    """
    Performs a deliberate out-of-bounds access to demonstrate catching
    any generic Exception and printing its message.
    """
    try:
        # This will trigger an IndexError
        value: int = SAMPLE_LIST[INDEX_TO_ACCESS]
        print(f"Value found: {value}")
        
    except Exception as e:
        # Catching base Exception captures almost all non-system-exiting errors
        print(f"An unexpected error occurred: {type(e).__name__} - {e}")

if __name__ == "__main__":
    risky_operation()