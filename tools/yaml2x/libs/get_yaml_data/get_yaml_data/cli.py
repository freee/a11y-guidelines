# yaml2json/cli.py
"""
Command-line interface for YAML to JSON conversion tool.
"""

import sys
from pathlib import Path
from get_yaml_data.config import setup_configuration
from get_yaml_data.process_yaml import convert_yaml_to_json

def main() -> None:
    """
    Main CLI function that processes YAML files and generates JSON output.
    """
    try:
        # Get configuration
        settings = setup_configuration()
        
        # Convert YAML to JSON
        convert_yaml_to_json(
            basedir=settings['basedir'],
            base_url=settings['base_url'],
            output_file=settings['output_file'],
            publish=settings['publish']
        )
            
    except Exception as e:
        sys.exit(f"Error during conversion process: {str(e)}")

if __name__ == "__main__":
    main()
