"""
Module   : q37_append_to_file.py
Package  : python_basic.file_handling
Topics   : File Handling
Question 37: Append data to existing file.
"""

def append_data(file_path: str, additional_text: str) -> None:
    """
    Appends new text to the end of an existing file without overwriting current contents.
    """
    # The 'a' (append) mode places the pointer at the end of the file.
    # If the file does not exist, it will safely create a new one.
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{additional_text}\n")

def execute_file_append() -> None:
    """
    Captures text from the user and appends it to a target file.
    """
    target_file: str = input("Enter target filename (default: student_profile.txt): ").strip() or "student_profile.txt"
    
    try:
        new_data: str = input("Enter the text you want to append: ").strip()
        
        if not new_data:
            raise ValueError("Cannot append empty text.")
            
        append_data(target_file, new_data)
        print(f"\nSuccess! Data appended to '{target_file}'.")
        
    except ValueError as error_msg:
        print(f"Input Error: {error_msg}")
    except IOError as io_error:
        print(f"System Error: Could not modify the file. Details: {io_error}")

if __name__ == "__main__":
    execute_file_append()