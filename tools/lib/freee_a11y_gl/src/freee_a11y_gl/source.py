"""Source path utilities for accessibility guidelines data files.

This module provides utilities for locating and accessing various data files
including YAML guidelines, checks, FAQ files, and JSON configuration files.
"""

import os
from typing import Dict, Optional

DATA_DIR = 'data'
YAML_DIR = 'yaml'
JSON_DIR = 'json'


def get_src_path(basedir: Optional[str] = None) -> Dict[str, str]:
    """
    Get source file paths for various components.

    Args:
        basedir: Base directory containing data files.
                If None, value from settings will be used. If not in settings, defaults to '.'

    Returns:
        Dictionary containing paths for different types of source files
    """
    from .config import Config

    # Get value from settings if not provided
    effective_basedir = basedir if basedir is not None else Config.get_basedir()
    data_basedir = os.path.join(effective_basedir, DATA_DIR)
    yaml_basedir = os.path.join(data_basedir, YAML_DIR)
    json_basedir = os.path.join(data_basedir, JSON_DIR)

    src_path = {
        'guidelines': os.path.join(yaml_basedir, "gl"),
        'checks': os.path.join(yaml_basedir, 'checks'),
        'faq': os.path.join(yaml_basedir, 'faq'),
        'wcag_sc': os.path.join(json_basedir, 'wcag-sc.json'),
        'gl_categories': os.path.join(json_basedir, 'guideline-categories.json'),
        'faq_tags': os.path.join(json_basedir, 'faq-tags.json'),
        'info': os.path.join(json_basedir, 'info.json')
    }
    return src_path
