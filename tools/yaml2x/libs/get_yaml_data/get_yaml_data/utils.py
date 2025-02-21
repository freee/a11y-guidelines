"""
Utility functions for YAML to JSON conversion.

This module provides utility functions for handling version information
and info links processing from pickle files.
"""

import pickle
from pathlib import Path
from typing import Dict, Any, List

# Constants
LANGUAGES: List[str] = ['ja', 'en']
PICKLE_PATH: str = 'build/doctrees/environment.pickle'

class UtilsError(Exception):
    """Custom exception for utility-related errors."""
    pass

def get_info_links(basedir: str, baseurl: str = '') -> Dict[str, Any]:
    """
    Extract labels and links from the environment pickle file.
    
    Args:
        basedir: Project root directory containing language-specific data
        baseurl: Base URL for related information links
        
    Returns:
        Dictionary containing extracted labels and their associated information
        
    Raises:
        UtilsError: If pickle file cannot be loaded or processed
    """
    info: Dict[str, Dict[str, Dict[str, str]]] = {}
    path_prefix = {
        'ja': '',
        'en': 'en/'
    }
    
    for lang in LANGUAGES:
        pickle_path = Path(basedir) / lang / PICKLE_PATH
        try:
            with open(pickle_path, 'rb') as f:
                doctree = pickle.load(f)
        except Exception as e:
            raise UtilsError(f'Failed to load pickle file {pickle_path}: {str(e)}')
            
        labels = doctree.domaindata['std']['labels']
        for label in labels:
            if not all(labels[label][i] for i in range(3)):
                continue
                
            if label not in info:
                info[label] = {
                    'text': {},
                    'url': {}
                }
            info[label]['text'][lang] = labels[label][2]
            info[label]['url'][lang] = f'{baseurl}/{path_prefix[lang]}{labels[label][0]}.html#{labels[label][1]}'

    return info

def get_version_info(basedir: str) -> Dict[str, str]:
    """
    Extract version information from version.py file.
    
    Args:
        basedir: Base directory containing version.py
        
    Returns:
        Dictionary containing version information
        
    Raises:
        UtilsError: If version file cannot be read or executed
    """
    try:
        version_data: Dict[str, str] = {}
        version_file = Path(basedir) / 'version.py'
        
        if not version_file.is_file():
            raise UtilsError(f"Version file not found: {version_file}")
            
        with open(version_file, encoding='utf-8') as f:
            exec(f.read(), version_data)
            
        return version_data
    except Exception as e:
        raise UtilsError(f"Failed to read version information: {str(e)}")
