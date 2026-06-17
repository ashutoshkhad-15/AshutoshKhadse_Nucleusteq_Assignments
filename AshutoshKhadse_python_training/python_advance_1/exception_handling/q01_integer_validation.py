"""
Q1: Write a program that takes a number as input and handles ValueError if the input is not a valid integer.

"""
# Constants
PROMPT_MESSAGE: str = "Please enter a valid integer: "

def get_integer_from_user(prompt: str) -> int:
    """
    Continuously prompts the user until a valid integer is provided.
    Handles ValueError if the conversion fails.
    """
    while True:
        user_input: str = input(prompt)
        try:
            valid_integer: int = int(user_input)
            print(f"Success! You entered: {valid_integer}")
            return valid_integer
        except ValueError:
            print("Error: That is not a valid integer. Please try again.")

if __name__ == "__main__":
    get_integer_from_user(PROMPT_MESSAGE)