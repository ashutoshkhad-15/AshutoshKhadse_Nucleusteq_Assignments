"""
2. Write a program to divide two numbers entered by the user and handle ZeroDivisionError.

"""
# Constants
PROMPT_NUMERATOR: str = "Enter the numerator (integer): "
PROMPT_DENOMINATOR: str = "Enter the denominator (integer): "

def perform_safe_division() -> None:
    """
    Prompts the user for two numbers and divides them, gracefully 
    handling attempts to divide by zero.
    """
    try:
        numerator: int = int(input(PROMPT_NUMERATOR))
        denominator: int = int(input(PROMPT_DENOMINATOR))
        
        result: float = numerator / denominator
        print(f"The result of {numerator} / {denominator} is {result:.2f}")
        
    except ZeroDivisionError:
        print("Error: Division by zero is undefined and not allowed.")
    except ValueError:
        print("Error: Please ensure you are entering valid integers.")

if __name__ == "__main__":
    perform_safe_division()