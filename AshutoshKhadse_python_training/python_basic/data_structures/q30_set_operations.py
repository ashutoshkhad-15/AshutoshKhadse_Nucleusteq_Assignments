"""
Module   : q30_set_operations.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 30: Perform union, intersection, and difference on two sets.
"""

from typing import Set, Dict

def perform_set_operations(set_a: Set[int], set_b: Set[int]) -> Dict[str, Set[int]]:
    """
    Executes core mathematical set operations. Sets are highly optimized in Python
    using hash tables, making these operations significantly faster than list comprehensions.
    """
    return {
        "Union (All unique elements)": set_a.union(set_b),
        "Intersection (Common in both)": set_a.intersection(set_b),
        "Difference (In A but not B)": set_a.difference(set_b),
        "Symmetric Diff (In either, not both)": set_a.symmetric_difference(set_b)
    }

def execute_set_operations() -> None:
    """
    Demonstrates set theory using predefined datasets representing user IDs.
    """
    print(" Mathematical Set Operations ")
    
    # Predefined sets for demonstration
    group_a: Set[int] = {1, 2, 3, 4, 5}
    group_b: Set[int] = {4, 5, 6, 7, 8}
    
    print(f"Set A: {group_a}")
    print(f"Set B: {group_b}\n")
    
    results = perform_set_operations(group_a, group_b)
    
    for operation, result_set in results.items():
        print(f"{operation:<38}: {result_set}")

if __name__ == "__main__":
    execute_set_operations()