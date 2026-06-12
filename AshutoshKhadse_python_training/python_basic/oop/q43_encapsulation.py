"""
Module   : q43_encapsulation.py
Package  : python_basic.oop
Topics   : Object-Oriented Programming (OOP)
Question 43: Implement encapsulation using private variables in Bank class.
"""

class BankAccount:
    """
    Demonstrates encapsulation by restricting direct access to the balance variable.
    """
    def __init__(self, account_holder: str, initial_balance: float) -> None:
        self.account_holder: str = account_holder
        
        # The double underscore (__) triggers name mangling in Python,
        # effectively making this attribute "private" and inaccessible from the outside.
        self.__balance: float = initial_balance

    # Getter Method (Controlled Access)
    def get_balance(self) -> float:
        """Returns the current balance securely."""
        return self.__balance

    # Setter Method (Controlled Mutation)
    def deposit(self, amount: float) -> None:
        """Allows adding funds with validation logic."""
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount:.2f}. New Balance: ${self.__balance:.2f}")
        else:
            print("Error: Deposit amount must be positive.")

    def withdraw(self, amount: float) -> None:
        """Allows removing funds with strict boundary checks."""
        if amount > self.__balance:
            print("Transaction Failed: Insufficient funds.")
        elif amount <= 0:
            print("Error: Withdrawal amount must be positive.")
        else:
            self.__balance -= amount
            print(f"Withdrew ${amount:.2f}. Remaining Balance: ${self.__balance:.2f}")

def execute_encapsulation() -> None:
    """
    Shows how encapsulation protects data from unauthorized modifications.
    """
    
    my_account = BankAccount("Ashutosh Khadse", 5000.00)
    print(f"Account Owner : {my_account.account_holder}")
    
    # Secure interactions via public methods
    my_account.deposit(1500.00)
    my_account.withdraw(800.00)
    my_account.withdraw(10000.00)  # This will be blocked by internal validation
    
    # Attempting to print my_account.__balance here would throw an AttributeError!

if __name__ == "__main__":
    execute_encapsulation()