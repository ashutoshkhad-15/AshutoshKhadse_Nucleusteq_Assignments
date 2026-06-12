"""
Module   : q20_default_parameters.py
Package  : python_basic.functions
Topics   : Functions
Question 20: Write a function using default parameters.
"""

def generate_profile(name: str, role: str = "Trainee", company: str = "NucleusTeq") -> str:
    """
    Generates a professional profile string.
    Demonstrates the use of default parameters to increase function reusability.
    """
    return f"Profile: {name} | Role: {role} | Company: {company}"

def execute_profile_generator() -> None:
    """
    Interactively captures profile data and handles empty input errors.
    """
    
    try:
        user_name: str = input("Enter your first name (Required): ").strip()
        
        if not user_name:
            # Raising an error ensures the core parameter is always present
            raise ValueError("The 'name' parameter is strictly required.")
            
        print("\n Generating Profiles ")
        # 1. Using all default parameters
        print("1. Defaults Applied   :", generate_profile(user_name))
        
        # 2. Overriding a single default parameter
        print("2. Role Overridden    :", generate_profile(user_name, role="Data Software Engineer"))
        
        # 3. Overriding all default parameters
        print("3. All Overridden     :", generate_profile(user_name, "Senior Engineer", "Google"))
        
    except ValueError as error_message:
        print(f"Input Error: {error_message}")

if __name__ == "__main__":
    execute_profile_generator()