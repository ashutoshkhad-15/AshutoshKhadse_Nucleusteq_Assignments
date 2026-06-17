"""
4. Handle multiple exceptions  in a single program.

"""
from typing import List, Any

# Constants
MIXED_DATA: List[Any] = ["10", "zero", 0, "20"]

def process_mixed_data(data: List[Any]) -> None:
    """
    Iterates through a list and attempts to divide 100 by each parsed integer.
    Catches multiple specific exceptions in one block.
    """
    base_value: int = 100
    
    for item in data:
        try:
            divisor: int = int(item)
            result: float = base_value / divisor
            print(f"{base_value} / {divisor} = {result}")
            
        except (ValueError, TypeError):
            # Catches issues with parsing strings like "zero" or invalid types
            print(f"Data Error: Cannot convert '{item}' to a valid integer.")
            
        except ZeroDivisionError:
            # Catches division by zero specifically
            print(f"Math Error: Attempted to divide {base_value} by zero.")

if __name__ == "__main__":
    process_mixed_data(MIXED_DATA)