"""
Module   : q28_tuple_access.py
Package  : python_basic.data_structures
Topics   : Tuple, Set & Dictionary
Question 28: Create a tuple and access elements.
"""

from typing import Tuple

def demonstrate_tuple_access() -> None:
    """
    Create a tuple of student exam scores and demonstrate common access patterns:
    indexing, negative indexing, and slicing.

    Tuples are immutable sequences — ideal for data that should not change.
    """
    student_scores: Tuple[int, ...] = (85, 92, 78, 95, 60, 88, 74)

    print(f"  Tuple                  : {student_scores}")
    print(f"  First score  [0]       : {student_scores[0]}")
    print(f"  Last score   [-1]      : {student_scores[-1]}")
    print(f"  Scores [1:4]           : {student_scores[1:4]}")
    print(f"  Length                 : {len(student_scores)}")
    print(f"  Min / Max              : {min(student_scores)} / {max(student_scores)}")
    
if __name__ == "__main__":
    demonstrate_tuple_access()