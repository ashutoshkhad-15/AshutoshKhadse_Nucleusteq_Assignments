"""
Module   : q24_nexus_fleet_utils.py
Package  : python_basic.modules
Topics   : Modules
Purpose  : A custom utility module to be imported by q24_custom_module_import.py
"""

def calculate_rental_estimate(days: int, daily_rate: float) -> float:
    """
    Calculates the total cost of a vehicle rental.
    """
    if days < 1:
        raise ValueError("Rental period must be at least 1 day.")
    if daily_rate < 0:
        raise ValueError("Daily rate cannot be negative.")
        
    return days * daily_rate

def get_fleet_status() -> str:
    """
    Returns a standard system status string.
    """
    return "NexusFleet System: All vehicles are currently operational."