import sys
import os
import logging
import argparse
from typing import Optional
from pathlib import Path
from .auth import GoogleAuthManager
from .sheet_generator import ChecklistSheetGenerator
from .config_loader import load_configuration, ApplicationConfig, create_default_config
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from freee_a11y_gl import settings as GL
from freee_a11y_gl.yaml_processor import process_yaml_data

def parse_args() -> argparse.Namespace:
    """Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Generate checklist in Google Sheets',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a default configuration file in the current directory and exit.'
    )
    
    parser.add_argument(
        '-c', '--config',
        type=str,
        help='Path to configuration file (supported formats: yaml, toml, ini)'
    )
    
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize spreadsheet (warning: removes existing sheets)'
    )
    
    parser.add_argument(
        '-p', '--production',
        action='store_true',
        help='Use production spreadsheet (default: use development spreadsheet)'
    )
    
    parser.add_argument(
        '-b', '--basedir',
        type=str,
        default=str(Path.cwd()),
        help='The root directory of the Guidelines project (default: current working directory)'
    )

    parser.add_argument(
        '--url',
        type=str,
        help='Base URL for documentation links (default: from config file)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging (overrides config log level)'
    )
    
    return parser.parse_args()

def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging with the specified level
    
    Args:
        level: Logging level to use
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True  # Override existing handlers
    )

def get_credentials(config: ApplicationConfig) -> Optional[Credentials]:
    """Get Google API credentials
    
    Args:
        config: Application configuration
        
    Returns:
        Optional[Credentials]: Google API credentials or None if authentication fails
    """
    logger = logging.getLogger(__name__)
    auth_manager = GoogleAuthManager(
        credentials_path=config.credentials_path.as_posix(),
        token_path=config.token_path.as_posix()
    )
    
    try:
        credentials = auth_manager.get_credentials()
        logger.info("Authentication successful")
        return credentials
    except FileNotFoundError as e:
        # Treat missing credential file as an error
        if str(e).startswith("Credentials file not found"):
            logger.error(f"Authentication error: {e}")
            logger.error(f"Please download credentials.json from Google Cloud Console")
            return None
        # Missing token file is normal for first run - continue processing
        logger.debug(f"Token file not found (this is normal for first run): {e}")
        credentials = None
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None
        
    return credentials

def main() -> int:
    """Main entry point for the application
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # Set up initial logging with default level
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    args = parse_args()
    
    # Set verbose logging if requested
    if args.verbose:
        setup_logging(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    if args.create_config:
        try:
            output_path = Path.cwd() / "yaml2sheet.yaml"
            created_path = create_default_config(output_path)
            logger.info(f"Default configuration file created at: {created_path}")
            print(f"Default configuration file created at: {created_path}")
            print("Please edit this file with your settings and run the command again.")
            return 0
        except Exception as e:
            logger.error(f"Failed to create configuration file: {e}")
            return 1
    
    try:
        # Load configuration
        logger.debug(f"Loading configuration from {args.config if args.config else 'default locations'}")
        config = load_configuration(args.config)

    except FileNotFoundError:
        logger.warning("Configuration file not found.")
        if not args.config and sys.stdout.isatty():
            try:
                response = input("Would you like to create a default configuration file (config.yaml)? [y/N]: ")
                if response.lower().strip() == 'y':
                    output_path = Path.cwd() / "yaml2sheet.yaml"
                    created_path = create_default_config(output_path)
                    print(f"\nDefault configuration file created at: {created_path}")
                    print("Please edit this file with your settings and run the command again.")
                    return 0
                else:
                    print("Aborting. Please create a configuration file manually.")
                    return 1
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled.")
                return 1
        else:
            logger.error("No configuration file found at the specified path or default locations.")
            return 1

    # Update log level from config if not in verbose mode
    if not args.verbose:
        current_level = logging.getLogger().getEffectiveLevel()
        config_level = config.get_log_level()
        if current_level != config_level:
            logger.debug(f"Updating log level from {current_level} to {config_level}")
            setup_logging(config_level)
    
    # Log which environment we're using
    env_type = "production" if args.production else "development"
    logger.info(f"Using {env_type} environment")
    
    # Get authentication
    credentials = get_credentials(config)
    if credentials is None:
        return 1

    try:
        # Get base directory using unified handler
        source_path = config.get_basedir(args.basedir)
        logger.info(f"Using base directory: {source_path}")

        # Set base URL from command line or config
        base_url = args.url or config.get_base_url()
        GL.update({'base_url': base_url})
        logger.info(f"Using base URL: {base_url}")

        # Process source YAML data
        logger.info(f"Processing YAML data from {source_path}")
        source_data = process_yaml_data(str(source_path))
        logger.info(f"Processed {len(source_data.get('checks', {}))} checks from source data")
        
    except Exception as e:
        logger.error(f"Failed to load source data: {e}")
        return 1

    try:
        # Get appropriate spreadsheet ID
        spreadsheet_id = config.get_spreadsheet_id(args.production)
        logger.info(f"Using spreadsheet ID: {spreadsheet_id}")

        editor_email = config.sheet_editor_email
        logger.info(f"Using editor email: {editor_email}")

        if credentials is None:
            logger.error("No valid credentials available. Please run the script again to authenticate.")
            return 1

        # Generate checklist
        logger.info(f"Starting checklist generation in {env_type} environment")
        generator = ChecklistSheetGenerator(credentials, spreadsheet_id, editor_email)
        generator.generate_checklist(source_data, initialize=args.init)
        logger.info(f"Checklist generation completed successfully")
        return 0
        
    except HttpError as e:
        logger.error(f"Google API error: {e.reason} (status: {e.status_code})")
        if e.status_code == 403:
            logger.error("Permission denied. Check your credentials and ensure you have access to the spreadsheet.")
        return 1
    except Exception as e:
        logger.error(f"Failed to generate checklist: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
