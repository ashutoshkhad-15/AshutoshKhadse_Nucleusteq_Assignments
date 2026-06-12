"""
Module   : q10_grade_calculator.py
Package  : python_basic.operators_conditionals
Topics   : Python Basics – Operators & Conditionals
Question 10: Calculate grade based on marks (A/B/C/Fail).
"""

def calculate_grade(marks: float) -> str:
    """
    Return the letter grade corresponding to the marks scored.
    """
    # Conditionals are evaluated top-to-bottom. We start with the highest threshold 
    # so we do not need to check upper bounds (e.g., no need for `marks >= 80 and marks < 90`).
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    else:
        return "Fail"


def execute_grade_calculator() -> None:
    """
    Takes student marks as input and displays the calculated grade.
    """
    student_marks: float = float(input("Enter the student's total marks (0-100): "))
    
    # Preventing illogical inputs strictly for boundary safety
    if student_marks < 0 or student_marks > 100:
        print("Invalid entry: Marks must be between 0 and 100.")
        return

    final_grade: str = calculate_grade(student_marks)
    print(f"Marks: {student_marks} -> Grade: {final_grade}")


if __name__ == "__main__":
    execute_grade_calculator()