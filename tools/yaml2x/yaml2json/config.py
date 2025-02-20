"""
Configuration module for YAML to JSON conversion.

This module handles command-line argument parsing and configuration
setup for the YAML to JSON conversion process.
"""

import argparse
from pathlib import Path
from typing import Dict, Any

# Default values
DEFAULT_OUTPUT_FILE: str = 'data.json'
DEFAULT_BASE_URL: str = ''
DEFAULT_BASE_DIR: str = '.'

class ConfigError(Exception):
    """Custom exception for configuration-related errors."""
    pass

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the conversion process.
    
    Returns:
        Namespace containing parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Process YAML files and generate a JSON file containing checklist items."
    )
    parser.add_argument(
        '--basedir', '-b',
        type=str,
        default=DEFAULT_BASE_DIR,
        help='Base directory where the data directory is located.'
    )
    parser.add_argument(
        '--output-file', '-o',
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help='Output file path.'
    )
    parser.add_argument(
        '--base-url', '-u',
        type=str,
        default=DEFAULT_BASE_URL,
        help='Base URL for the links to related information.'
    )
    parser.add_argument(
        '--publish', '-p',
        action='store_true',
        help='Generate for publishing'
    )
    return parser.parse_args()

def process_arguments(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Process the command-line arguments and validate paths.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Dictionary containing validated settings
        
    Raises:
        ConfigError: If required paths are invalid
    """
    try:
        basedir = Path(args.basedir).resolve()
        if not basedir.is_dir():
            raise ConfigError(f"Base directory does not exist: {basedir}")

        if Path(args.output_file).is_absolute():
            output_file = Path(args.output_file)
        else:
            output_file = basedir / args.output_file
            
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        return {
            'basedir': str(basedir),
            'output_file': str(output_file),
            'base_url': args.base_url,
            'publish': args.publish
        }
    except Exception as e:
        raise ConfigError(f"Error processing arguments: {str(e)}")

def setup_configuration() -> Dict[str, Any]:
    """
    Set up and validate all configuration parameters.
    
    Returns:
        Dict containing validated configuration
    
    Raises:
        ConfigError: If required configuration is invalid
    """
    args = parse_args()
    return process_arguments(args)
