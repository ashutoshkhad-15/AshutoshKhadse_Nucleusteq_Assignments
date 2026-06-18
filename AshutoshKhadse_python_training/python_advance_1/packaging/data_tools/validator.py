def is_non_empty(text: str) -> bool:
    """Checks if a string is not empty or composed purely of whitespace."""
    return bool(text and text.strip())