"""
Module   : q03_user_greeting.py
Package  : python_basic.introduction
Topics   : Introduction to Python
Question 3 : Take user input (name and age) and print a formatted message.
"""
def greet_user() -> None:
    """
    Prompt the user for their name and age, then print a formatted greeting.
    Uses f-strings for clean, readable string interpolation.
    """
    name: str = input("Enter your name : ").strip()
    age_input: str = input("Enter your age  : ").strip()

    # Validate that age is a valid integer before converting
    if not age_input.isdigit():
        print("Invalid age entered. Please enter a whole number.")
        return

    age: int = int(age_input)
    print(f"\nHello, {name}! You are {age} years old.")
    print(f"Welcome to the Python training program, {name}!")

if __name__ == "__main__":
    greet_user()