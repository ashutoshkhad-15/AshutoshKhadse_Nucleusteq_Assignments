"""
Module   : q06_basic_arithmetic.py
Package  : python_basic.variables_datatypes
Topics   : Python Basics – Variables & Data Types
Question 6 : Take two numbers and print sum, difference, multiplication, and division.
"""

def perform_arithmetic(first: float, second: float) -> None:
    """
    Calculate and display the sum, difference, product, and quotient of two numbers.

    Guards against division by zero before attempting division.

    Args:
        first  : The first operand.
        second : The second operand.
    """
    print(f"  Inputs          : {first} and {second}")
    print(f"  Sum             : {first} + {second} = {first + second}")
    print(f"  Difference      : {first} - {second} = {first - second}")
    print(f"  Multiplication  : {first} × {second} = {first * second}")

    if second != 0:
        print(f"  Division        : {first} ÷ {second} = {first / second:.4f}")
        print(f"  Floor Division  : {first} // {second} = {first // second}")
        print(f"  Modulus         : {first} % {second}  = {first % second}")
    else:
        print("  Division        : Cannot divide by zero.")

if __name__ == "__main__":
    num1: float = float(input("Enter first number: "))
    num2: float = float(input("Enter second number: "))
    perform_arithmetic(num1, num2)