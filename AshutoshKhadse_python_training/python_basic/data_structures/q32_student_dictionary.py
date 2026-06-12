"""
Module   : q32_student_dictionary.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 32: Create a student dictionary and access values.
"""

from typing import Dict, Any

def create_student_record() -> None:
    """
    Creates a dictionary and demonstrates robust methods for accessing its values.
    """
    
    # Dictionaries store data in key-value pairs with O(1) lookup time.
    student_record: Dict[str, Any] = {
        "student_id": "NTQ-1045",
        "name": "Ashutosh",
        "course": "Data Engineering",
        "grade": "A"
    }
    
    print("1. Standard Bracket Access:")
    # Bracket notation is fast but will throw a KeyError if the key does not exist.
    print(f"   Name   : {student_record['name']}")
    print(f"   Course : {student_record['course']}\n")
    
    print("2. Safe Access using .get():")
    # The .get() method is the industry standard for safe dictionary lookups because 
    # it prevents application crashes by returning None (or a default value) if the key is missing.
    phone_number = student_record.get("phone_number", "No phone number on file")
    print(f"   Phone  : {phone_number}")

if __name__ == "__main__":
    create_student_record()