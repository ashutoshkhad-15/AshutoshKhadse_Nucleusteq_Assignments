"""
Module   : q35_write_name_file.py
Package  : python_basic.file_handling
Topics   : File Handling
Question 35: Create a file and write your name into it.
"""

# Defining the target filename as a constant to avoid hardcoding strings deep in the logic.
DEFAULT_FILE_NAME: str = "student_profile.txt"

def write_name_to_file(name: str, file_path: str) -> None:
    """
    Creates a new file (or overwrites an existing one) and writes the provided name into it.
    """
    # Using the 'with' statement (context manager) is the industry standard because it 
    # guarantees the file is properly closed and memory is released even if an error occurs.
    # The 'w' mode creates the file if it does not exist.
    # Specifying encoding='utf-8' prevents cross-platform text corruption.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Student Name: {name}\n")

def execute_file_write() -> None:
    """
    Captures user input and executes the file writing operation.
    """
    
    try:
        user_name: str = input("Enter your full name to write to the file: ").strip()
        
        if not user_name:
            raise ValueError("Name cannot be empty.")
            
        write_name_to_file(user_name, DEFAULT_FILE_NAME)
        print(f"\nSuccess! '{user_name}' has been written to '{DEFAULT_FILE_NAME}'.")
        
    except ValueError as error_msg:
        print(f"Input Error: {error_msg}")
    except IOError as io_error:
        # Catching IOError handles unexpected OS-level issues like permission denials.
        print(f"System Error: Could not write to file. Details: {io_error}")

if __name__ == "__main__":
    execute_file_write()