"""
Module   : q40_student_class.py
Package  : python_basic.oop
Topics   : Object-Oriented Programming (OOP)
Question 40: Create a Student class with attributes and display details.
"""

class Student:
    """
    Represents a student entity with core academic attributes.
    
    Attributes:
        name       (str)  : Full name of the student.
        age        (int)  : Age in years.
        student_id (str)  : Unique enrolment identifier.
    """
    
    def __init__(self, name: str, age: int, student_id: str) -> None:
        """
        Constructor initializes the Student object with required state.
        
        Args:
            name       : Full name.
            age        : Age (must be positive).
            student_id : Unique ID string.
        """
        
        # 'self' binds these attributes strictly to the instantiated object
        self.name: str = name
        self.age: int = age
        self.student_id: str = student_id

    def display_details(self) -> None:
        """
        Outputs the internal state of the student object to the console.
        """
        print(" Student Record ")
        print(f"Name   : {self.name}")
        print(f"Age    : {self.age}")
        print(f"Student ID : {self.student_id}\n")

def execute_student_class() -> None:
    """
    Demonstrates instantiation and method execution of the Student class.
    """
    # Creating an instance of the Student class
    student_one = Student("Ashutosh", 23, "EN22CS301220")
    
    # Invoking the instance method
    student_one.display_details()

if __name__ == "__main__":
    execute_student_class()