"""
YAML to JSON converter package for accessibility guidelines.

This package provides functionality to convert YAML-based accessibility
guidelines into JSON format, handling RST markup and multilingual content.
"""

from .process_yaml import get_yaml_data
from .process_yaml import convert_yaml_to_json

__all__ = ['get_yaml_data', 'convert_yaml_to_json']

# Version information
__version__ = '0.1.0'
