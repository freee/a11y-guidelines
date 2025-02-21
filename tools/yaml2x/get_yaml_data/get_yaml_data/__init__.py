"""
YAML to JSON converter package for accessibility guidelines.

This package provides functionality to convert YAML-based accessibility
guidelines into JSON format, handling RST markup and multilingual content.
"""

from . import config, utils, rst_processor
from .yaml2json import main

__all__ = [
    'main',           # Main conversion function
    'config',         # Configuration handling
    'utils',          # Utility functions
    'rst_processor',  # RST markup processing
]

# Version information
__version__ = '0.1.0'
