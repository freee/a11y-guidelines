# get_yaml_data.py
"""
Main module for YAML processing and conversion to JSON.

This module provides the core functionality for converting YAML files to JSON format,
focusing on accessibility guidelines processing.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

from freee_a11y_gl import (
    setup_instances, InfoRef, Check,
    info_utils, get_version_info
)
from .config import setup_configuration
from . import rst_processor

def get_yaml_data(basedir: Optional[str] = None, base_url: Optional[str] = None, publish: bool = False) -> Dict[str, Any]:
    """
    Process YAML files and return structured data as a Python dictionary.

    Args:
        basedir (Path): Base directory containing YAML files
        base_url (str): Base URL for links
        publish (bool): Flag to indicate if this is a publication build

    Returns:
        Dict[str, Any]: Processed data including version info, checks, and conditions

    Raises:
        Exception: If there's an error during the conversion process
    """
    # Get version info and setup instances with basedir
    version_info: Dict[str, str] = get_version_info(basedir)
    setup_instances(basedir)

    # Process information links and references
    info_links: Dict[str, Any] = info_utils.get_info_links(basedir, base_url)
    for info in InfoRef.list_all_internal():
        if info.ref in info_links:
            info.set_link(info_links[info.ref])
    
    # Process checks and their conditions
    checks: Dict[str, Any] = Check.object_data_all(base_url)
    for key in checks:
        if 'conditions' in checks[key]:
            checks[key]['conditions'] = [
                rst_processor.process_rst_condition(condition, info_links) 
                for condition in checks[key]['conditions']
            ]

    # Return output data
    return {
        'publish': publish,
        'version': version_info['checksheet_version'],
        'date': version_info['checksheet_date'],
        'checks': checks
    }

def convert_yaml_to_json(
    basedir: Optional[str] = None,
    base_url: Optional[str] = None,
    output_file: Optional[str] = None,
    publish: bool = False
) -> None:
    """
    Convert YAML files to JSON and write to specified output file.

    Args:
        basedir (Path): Base directory containing YAML files
        base_url (str): Base URL for links
        output_file (Path): Path to output JSON file
        publish (bool): Flag to indicate if this is a publication build

    Raises:
        Exception: If there's an error during the conversion process
    """
    try:
        # Process YAML data
        output_data = get_yaml_data(basedir, base_url, publish)
        
        # Write to JSON file if output_file is provided
        if output_file is not None:
            with open(output_file, mode="w", encoding="utf-8", newline="\n") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        raise Exception(f"Error during conversion process: {str(e)}")
