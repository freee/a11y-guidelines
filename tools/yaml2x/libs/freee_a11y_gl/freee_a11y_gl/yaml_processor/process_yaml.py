"""
Main module for YAML processing and conversion to JSON.

This module provides the core functionality for converting YAML files to JSON format,
focusing on accessibility guidelines processing.
"""

from typing import Dict, Any, Optional

from freee_a11y_gl import (
    InfoRef,
    Check,
    info_utils,
    get_version_info,
    Config,
    setup_instances
)
from . import rst_processor

def process_yaml_data(basedir: Optional[str] = None) -> Dict[str, Any]:
    """
    Process YAML files and return structured data as a Python dictionary.

    Args:
        basedir (str, optional): Base directory containing YAML files

    Returns:
        Dict[str, Any]: Processed data including version info, checks, and conditions

    Raises:
        Exception: If there's an error during the conversion process
    """
    # Get version info and setup instances with basedir
    version_info: Dict[str, str] = get_version_info(basedir)
    setup_instances(basedir)

    # Process information links and references
    info_links: Dict[str, Any] = info_utils.get_info_links(basedir)
    for info in InfoRef.list_all_internal():
        if info.ref in info_links:
            info.set_link(info_links[info.ref])
    
    # Process checks and their conditions
    checks: Dict[str, Any] = Check.object_data_all()
    for key in checks:
        if 'conditions' in checks[key]:
            checks[key]['conditions'] = [
                rst_processor.process_rst_condition(condition, info_links) 
                for condition in checks[key]['conditions']
            ]

    # Return output data
    return {
        'version': version_info['checksheet_version'],
        'date': version_info['checksheet_date'],
        'checks': checks
    }
