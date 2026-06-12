"""
Module   : q44_polymorphism.py
Package  : python_basic.oop
Topics   : Object-Oriented Programming (OOP)
Question 44: Demonstrate polymorphism using different classes with the same method name.
"""

from typing import List

# Class 1
class PostgreSQLDatabase:
    """Represents a relational database system."""
    
    def process_data(self) -> str:
        # Method shared across different classes
        return "Executing standard SQL queries on structured relational data."

# Class 2
class HadoopCluster:
    """Represents a distributed big data file system."""
    
    def process_data(self) -> str:
        # Same method name, completely different internal implementation
        return "Running MapReduce jobs across distributed data nodes."

def execute_polymorphism() -> None:
    """
    Demonstrates polymorphism: calling the exact same method on different 
    object types and getting type-specific behavior.
    """
    
    # Instantiating different objects
    relational_db = PostgreSQLDatabase()
    big_data_fs = HadoopCluster()
    
    # Grouping them in a generic list. Because of polymorphism, Python doesn't 
    # care what class they belong to, as long as they implement 'process_data()'.
    data_systems: List[object] = [relational_db, big_data_fs]
    
    for system in data_systems:
        # Python dynamically resolves which method to call at runtime
        print(f"{system.__class__.__name__:<20} : {system.process_data()}")

if __name__ == "__main__":
    execute_polymorphism()