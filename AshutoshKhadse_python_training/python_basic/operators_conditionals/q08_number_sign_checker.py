"""
Module   : q08_number_sign_checker.py
Package  : python_basic.operators_conditionals
Topics   : Python Basics – Operators & Conditionals
Question 8 : Check whether a number is positive, negative, or zero.
"""

def check_number_sign(number: float) -> str:
    """
    Evaluates the mathematical sign of a given number.
    Args:
        number : The number to check.
    Returns:
        'Positive', 'Negative', or 'Zero'.
    """
    # Using an if-elif-else chain ensures only one condition is evaluated once a match is found,
    # optimizing the conditional flow.
    if number > 0:
        return "Positive"
    elif number < 0:
        return "Negative"
    else:
        return "Zero"


def execute_sign_checker() -> None:
    """
    Inputs a number from the user and outputs its sign.
    """
    user_num: float = float(input("Enter a number: "))
    
    sign: str = check_number_sign(user_num)
    print(f"The number {user_num} is {sign}.")


if __name__ == "__main__":
    execute_sign_checker()