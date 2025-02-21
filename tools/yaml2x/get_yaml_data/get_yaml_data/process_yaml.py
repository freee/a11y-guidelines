"""
Main module for YAML to JSON conversion.

This module orchestrates the conversion process, handling configuration,
data processing, and output generation for accessibility guidelines.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
sys.path.append(str(Path(__file__).resolve().parent.parent))

from a11y_guidelines import setup_instances, InfoRef, Check
import config, utils, rst_processor

def get_yaml_data(basedir: Path, base_url: str, publish: bool = False) -> Dict[str, Any]:
    """
    Process YAML files and return structured data as a Python dictionary.

    Args:
        basedir (Path): Base directory containing YAML files
        base_url (str): Base URL for links

    Returns:
        Dict[str, Any]: Processed data including version info, checks, and conditions

    Raises:
        Exception: If there's an error during the conversion process
    """
    # Initialize configuration
    settings: Dict[str, Any] = {
        "basedir": basedir,
        "base_url": base_url,
        "publish": publish
    }
    
    version_info: Dict[str, str] = utils.get_version_info(basedir)
    setup_instances(basedir)

    # Process information links and references
    info_links: Dict[str, Any] = utils.get_info_links(basedir, base_url)
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

def main() -> None:
    """
    Main CLI function that processes YAML files and generates JSON output.
    """
    try:
        # Get configuration
        settings: Dict[str, Any] = config.setup_configuration()
        
        # Process YAML data
        output_data = get_yaml_data(settings['basedir'], settings['base_url'], settings['publish'])
        
        # Write to JSON file
        with open(settings['output_file'], mode="w", encoding="utf-8", newline="\n") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        sys.exit(f"Error during conversion process: {str(e)}")

if __name__ == "__main__":
    main()
