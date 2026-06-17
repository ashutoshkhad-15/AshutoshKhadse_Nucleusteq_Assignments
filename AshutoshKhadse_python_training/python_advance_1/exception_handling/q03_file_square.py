"""
Write a program using try-except-else-finally to read a number from a file  and print its square.

"""
import os

# Constants
FILE_PATH: str = "number_data.txt"

def read_and_square_number(file_path: str) -> None:
    """
    Attempts to read a file, parse an integer, and print its square.
    Demonstrates the full try-except-else-finally block structure.
    """
    file_handle = None
    
    try:
        # For demonstration, creating a temporary file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("12")
                
        file_handle = open(file_path, 'r')
        content: str = file_handle.read().strip()
        number: int = int(content)
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError:
        print("Error: The file does not contain a valid integer.")
        
    else:
        # Executes ONLY if the try block succeeds without exceptions
        square: int = number ** 2
        print(f"The square of the number {number} from the file is {square}.")
        
    finally:
        # Executes NO MATTER WHAT, perfect for resource cleanup
        if file_handle and not file_handle.closed:
            file_handle.close()
            print("Cleanup: File handle closed.")

if __name__ == "__main__":
    read_and_square_number(FILE_PATH)