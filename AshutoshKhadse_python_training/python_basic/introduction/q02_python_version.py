"""
Module   : q02_python_version.py
Package  : python_basic.introduction
Topics   : Introduction to Python
Question 2 : Write a program to check your Python version.
"""

import sys

def display_python_version() -> None:
    """Display the Python interpreter version currently in use."""
    # sys.version is preferred here over sys.version_info because it provides 
    # a fully formatted, readable string that includes compiler details, 
    # which is ideal for environment verification.
    print(f"Python Version  : {sys.version}")

if __name__ == "__main__":
    display_python_version()