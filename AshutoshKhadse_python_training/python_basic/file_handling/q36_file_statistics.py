"""
Module   : q36_file_statistics.py
Package  : python_basic.file_handling
Topics   : File Handling
Question 36: Read a file and count words, lines, and characters.
"""

from typing import Dict

def calculate_file_statistics(file_path: str) -> Dict[str, int]:
    """
    Reads a text file and calculates the total number of lines, words, and characters.
    """
    stats: Dict[str, int] = {"Lines": 0, "Words": 0, "Characters": 0}
    
    # Opening in 'r' (read) mode. 
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stats["Lines"] += 1
            # len(line) includes spaces and newline characters, which is standard for char counts
            stats["Characters"] += len(line) 
            # .split() breaks the line into a list of words based on whitespace
            stats["Words"] += len(line.split())
            
    return stats

def execute_statistics_analyzer() -> None:
    """
    Requests a filename from the user and analyzes its contents.
    """
    
    # Pre-filling the default file we created in Q35 to make testing easier
    target_file: str = input("Enter the filename to analyze (default: student_profile.txt): ").strip()
    if not target_file:
        target_file = "student_profile.txt"
        
    try:
        file_stats = calculate_file_statistics(target_file)
        
        print(f"\n Statistics for '{target_file}' ")
        for metric, count in file_stats.items():
            print(f"{metric:<12}: {count}")
            
    except FileNotFoundError:
        # Explicitly handling the most common file operation error
        print(f"Error: The file '{target_file}' does not exist in the current directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    execute_statistics_analyzer()