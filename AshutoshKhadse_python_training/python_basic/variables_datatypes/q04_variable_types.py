"""
Module   : q04_variable_types.py
Package  : python_basic.variables_datatypes
Topics   : Python Basics – Variables & Data Types
Question 4 : Create variables of type int, float, string, and boolean. Print their types using type().
"""

def demonstrate_data_types() -> None:
    """
    Create variables of the four fundamental Python data types and display
    each value alongside its runtime type using the built-in type() function.
    """
    integer_value: int = 15
    float_value: float = 3.14159
    string_value: str = "Hello, World!"
    boolean_value: bool = True

    # We use type() inside an f-string to clearly display the variable's value alongside its class type.
    print(f"  integer_value = {integer_value!r:<20}  type → {type(integer_value)}")
    print(f"  float_value   = {float_value!r:<20}  type → {type(float_value)}")
    print(f"  string_value  = {string_value!r:<20}  type → {type(string_value)}")
    print(f"  boolean_value = {boolean_value!r:<20}  type → {type(boolean_value)}")

if __name__ == "__main__":
    demonstrate_data_types()