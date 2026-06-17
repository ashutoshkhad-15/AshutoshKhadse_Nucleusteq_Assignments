"""
8. Write a program that handles FileNotFoundError when trying to open a file.
"""
# Constants
MISSING_FILE: str = "configuration_settings_missing.json"

def read_configuration(file_path: str) -> None:
    """
    Attempts to open a configuration file and handles the scenario 
    where the file does not exist.
    """
    try:
        with open(file_path, 'r') as file:
            content: str = file.read()
            print("File read successfully.")
            
    except FileNotFoundError:
        print(f"Critical Error: The configuration file '{file_path}' is missing.")
        print("Please ensure the file exists in the directory before running.")

if __name__ == "__main__":
    read_configuration(MISSING_FILE)