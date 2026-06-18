"""
Initialize the data_tools package.
By importing these functions here, we allow users to import them directly 
from the package root (e.g., 'from data_tools import capitalize_words').
"""
from .formatter import capitalize_words
from .validator import is_non_empty