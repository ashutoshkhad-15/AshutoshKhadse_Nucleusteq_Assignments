"""
Module   : q39_search_word_file.py
Package  : python_basic.file_handling
Topics   : File Handling
Question 39: Search a word in a file.
"""

from typing import List

def search_in_file(file_path: str, search_term: str) -> List[int]:
    """
    Scans a text file line-by-line to find occurrences of a specific word.
    Returns a list of line numbers (1-indexed) where the word was found.
    """
    found_lines: List[int] = []
    
    # We convert the search term to lowercase to ensure the search is case-insensitive,
    # which provides a much better user experience.
    search_term_lower: str = search_term.lower()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # enumerate() cleanly tracks the line number while we iterate
        for line_number, line_content in enumerate(file, start=1):
            if search_term_lower in line_content.lower():
                found_lines.append(line_number)
                
    return found_lines

def execute_word_search() -> None:
    """
    Captures the target file and search term, and outputs the search results.
    """
    
    target_file: str = input("Enter filename to search (default: student_profile.txt): ").strip() or "student_profile.txt"
    word_to_find: str = input("Enter the word to search for: ").strip()
    
    if not word_to_find:
        print("Error: Search term cannot be empty.")
        return
        
    try:
        results: List[int] = search_in_file(target_file, word_to_find)
        
        print(f"\n Search Results for '{word_to_find}' ")
        if results:
            print(f"Word found on line(s): {', '.join(map(str, results))}")
        else:
            print("The word was not found in the file.")
            
    except FileNotFoundError:
        print(f"Error: The file '{target_file}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    execute_word_search()