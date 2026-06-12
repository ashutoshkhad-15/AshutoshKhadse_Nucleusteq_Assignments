"""
Module   : q23_random_generator.py
Package  : python_basic.modules
Topics   : Modules
Question 23: Generate random numbers using random module.
"""

import random

def display_random_generations() -> None:
    """
    Demonstrates various capabilities of the random module, including 
    floats, integers, and sequence choices.
    """
    
    # 1. Generate a random float between 0.0 and 1.0
    random_float: float = random.random()
    print(f"Random Float (0.0 to 1.0) : {random_float:.4f}")
    
    # 2. Generate a random integer within a specific inclusive range
    min_val, max_val = 1, 100
    random_int: int = random.randint(min_val, max_val)
    print(f"Random Integer ({min_val}-{max_val})   : {random_int}")
    
    # 3. Generate a random float within a specific range using uniform
    random_uniform: float = random.uniform(10.5, 50.5)
    print(f"Random Uniform (10.5-50.5): {random_uniform:.2f}")

if __name__ == "__main__":
    # No user input is required here as the prompt specifically asks to generate random data
    display_random_generations()