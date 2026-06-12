"""
Module   : q38_copy_file_content.py
Package  : python_basic.file_handling
Topics   : File Handling
Question 38: Copy content from one file to another.
"""

def copy_file_contents(source_path: str, destination_path: str) -> None:
    """
    Reads all data from a source file and writes it to a destination file.
    """
    # By opening both files in a single 'with' statement, we ensure memory 
    # is cleanly managed for both operations simultaneously.
    with open(source_path, 'r', encoding='utf-8') as source_file, \
         open(destination_path, 'w', encoding='utf-8') as dest_file:
         
        # .read() loads the entire file. For massive files (GBs), you would iterate line-by-line, 
        # but for fundamental training, reading the whole file is standard.
        dest_file.write(source_file.read())

def execute_file_copy() -> None:
    """
    Handles user input for source and destination file paths and executes the copy.
    """
    
    source: str = input("Enter the source filename (default: student_profile.txt): ").strip() or "student_profile.txt"
    destination: str = input("Enter the destination filename (e.g., backup.txt): ").strip()
    
    if not destination:
        print("Error: You must provide a destination filename.")
        return
        
    try:
        copy_file_contents(source, destination)
        print(f"\nSuccess! Contents copied from '{source}' to '{destination}'.")
        
    except FileNotFoundError:
        print(f"Error: The source file '{source}' could not be found.")
    except Exception as generic_error:
        print(f"An unexpected error occurred during the copy process: {generic_error}")

if __name__ == "__main__":
    execute_file_copy()