"""
Module   : q41_car_class.py
Package  : python_basic.oop
Topics   : Object-Oriented Programming (OOP)
Question 41: Create a Car class with a constructor.
"""

class Car:
    """
    Defines a blueprint for a vehicle, demonstrating constructor initialization.
    
    Args:
            brand      : Manufacturer name (e.g. 'Toyota').
            model     : Model name (e.g. 'Hilux').
            engine_type      : Type of engine (e.g. '3.0L Inline-6 Turbo').
    """
    
    # The __init__ method is Python's constructor, called automatically upon instantiation
    def __init__(self, brand: str, model: str, engine_type: str) -> None:
        self.brand: str = brand
        self.model: str = model
        self.engine_type: str = engine_type
        self.is_running: bool = False  # Default state attribute

    def start_engine(self) -> None:
        """
        Mutates the internal state of the object.
        """
        if not self.is_running:
            self.is_running = True
            print(f"The {self.brand} {self.model}'s {self.engine_type} engine roars to life! True enthusiast feel.")
        else:
            print(f"The {self.brand} {self.model} is already running.")

def execute_car_class() -> None:
    """
    Demonstrates creating a Car object and interacting with its methods.
    """
    
    # Instantiating the object via the constructor
    enthusiast_car = Car("BMW", "M340i", "3.0L Inline-6 Turbo")
    
    print(f"Vehicle registered: {enthusiast_car.brand} {enthusiast_car.model}")
    enthusiast_car.start_engine()


if __name__ == "__main__":
    execute_car_class()