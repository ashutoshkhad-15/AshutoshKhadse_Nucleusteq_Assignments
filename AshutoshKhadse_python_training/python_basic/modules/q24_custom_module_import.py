"""
Module   : q24_custom_module_import.py
Package  : python_basic.modules
Topics   : Modules
Question 24: Create your own module and import it.
"""

# Importing the custom module we just created.
# Using 'as' creates an alias, which is an industry best practice to keep code clean.
import q24_nexus_fleet_utils as fleet_utils

def execute_custom_import() -> None:
    """
    Demonstrates utilizing functions from a user-defined external module.
    """
    
    # Accessing a function from the imported module
    system_status: str = fleet_utils.get_fleet_status()
    print(f"Status check: {system_status}")
    
    print("\n Rental Cost Estimator ")
    try:
        rental_days: int = int(input("Enter number of days for rental: "))
        rate: float = float(input("Enter the daily vehicle rate: $"))
        
        # Accessing the calculation engine from the imported module
        total_cost: float = fleet_utils.calculate_rental_estimate(rental_days, rate)
        
        print(f"Total Estimated Cost: ${total_cost:.2f}")
        
    except ValueError as error_msg:
        print(f"Input Error: {error_msg}")

if __name__ == "__main__":
    execute_custom_import()