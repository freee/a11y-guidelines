"""
Version information utilities for accessibility guidelines.

This module provides utilities for handling version and metadata
information from the guidelines project.
"""

from pathlib import Path
from typing import Dict, Optional

class VersionError(Exception):
    """Custom exception for version-related errors."""
    pass

def get_version_info(basedir: Optional[str] = None) -> Dict[str, str]:
    """
    Extract version information from version.py file.
    
    Args:
        basedir: Base directory containing version.py.
                If None, value from settings will be used. If not in settings, defaults to '.'
        
    Returns:
        Dictionary containing version information
        
    Raises:
        VersionError: If version file cannot be read or executed
    """
    try:
        from .settings import settings

        from .config import Config

        version_data: Dict[str, str] = {}
        effective_basedir = basedir if basedir is not None else Config.get_basedir()
        version_file = Path(effective_basedir) / 'version.py'
        
        if not version_file.is_file():
            raise VersionError(f"Version file not found: {version_file}")
            
        with open(version_file, encoding='utf-8') as f:
            exec(f.read(), version_data)
            
        return version_data
    except Exception as e:
        raise VersionError(f"Failed to read version information: {str(e)}")
