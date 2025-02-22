"""
Version information utilities for accessibility guidelines.

This module provides utilities for handling version and metadata
information from the guidelines project.
"""

from pathlib import Path
from typing import Dict

class VersionError(Exception):
    """Custom exception for version-related errors."""
    pass

def get_version_info(basedir: str) -> Dict[str, str]:
    """
    Extract version information from version.py file.
    
    Args:
        basedir: Base directory containing version.py
        
    Returns:
        Dictionary containing version information
        
    Raises:
        VersionError: If version file cannot be read or executed
    """
    try:
        version_data: Dict[str, str] = {}
        version_file = Path(basedir) / 'version.py'
        
        if not version_file.is_file():
            raise VersionError(f"Version file not found: {version_file}")
            
        with open(version_file, encoding='utf-8') as f:
            exec(f.read(), version_data)
            
        return version_data
    except Exception as e:
        raise VersionError(f"Failed to read version information: {str(e)}")
