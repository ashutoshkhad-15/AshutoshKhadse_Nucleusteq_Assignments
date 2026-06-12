"""
Module   : q42_inheritance.py
Package  : python_basic.oop
Topics   : Object-Oriented Programming (OOP)
Question 42: Implement inheritance using Person and Employee class.
"""

# Base Class (Parent)
class Person:
    """
    A foundational class representing a generic human entity.
    """
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def introduce(self) -> str:
        return f"Hi, my name is {self.name} and I am {self.age} years old."

# Derived Class (Child)
class Employee(Person):
    """
    Inherits attributes and methods from the Person class while 
    extending it with professional attributes.
    """
    def __init__(self, name: str, age: int, role: str, company: str) -> None:
        # super() is used to call the parent class's constructor, avoiding code duplication
        super().__init__(name, age)
        
        # Child-specific attributes
        self.role: str = role
        self.company: str = company

    def display_professional_profile(self) -> None:
        """
        Demonstrates accessing both inherited and newly defined attributes.
        """
        # Can access self.name because it was inherited from Person
        print(f"[{self.company}] {self.name} - {self.role}")

def execute_inheritance() -> None:
    """
    Demonstrates the parent-child class relationship.
    """

    # Instantiating the derived class
    staff_member = Employee("Ashutosh", 23, "Data Engineer", "NucleusTeq")
    
    # Calling a method inherited from the Parent class
    print(staff_member.introduce())
    
    # Calling a method specific to the Child class
    staff_member.display_professional_profile()

if __name__ == "__main__":
    execute_inheritance()