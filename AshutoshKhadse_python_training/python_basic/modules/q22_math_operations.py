"""
Module   : q22_math_operations.py
Package  : python_basic.modules
Topics   : Modules
Question 22: Use math module to find square root, power, and factorial.
"""

import math

def use_math_module(number: float) -> None:
    """
    Showcase key functions from Python's built-in math module.
    Functions covered: sqrt, pow, factorial, floor, ceil, log.

    Args:
        number : The input value for the demonstrations (must be ≥ 1).
    """
    whole: int = int(number)

    print(f"  Input                : {number}")
    print(f"  math.sqrt({number})    = {math.sqrt(number):.6f}")
    print(f"  math.factorial({whole}) = {math.factorial(whole)}")
    print(f"  math.floor({number})   = {math.floor(number)}")
    print(f"  math.ceil({number})    = {math.ceil(number)}")
    print(f"  math.log({number})     = {math.log(number):.6f}  (natural log)")
    print(f"  math.log10({number})   = {math.log10(number):.6f}")

def run_math_program() -> None:
    """
    Handles user input safely and displays the math module calculations.
    """
    
    while True:
        try:
            base: float = float(input("Enter the base number: "))
            power: float = float(input("Enter the exponent (power): "))
            
            use_math_module(base)
            
            print(f"\n Results for Base: {base} ")
            print(f"  math.pow({base}, {power})  = {math.pow(base, power):.2f}")

            break  # Exit loop on success
            
        except ValueError:
            print("Error: Please enter valid numeric values.")

if __name__ == "__main__":
    run_math_program()