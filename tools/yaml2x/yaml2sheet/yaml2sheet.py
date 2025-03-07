import sys
import os
import logging
import argparse
from pathlib import Path
from auth import GoogleAuthManager
from sheet_generator import ChecklistSheetGenerator
from config_loader import load_configuration
#sys.path.append(str(Path(__file__).resolve().parent.parent))

from freee_a11y_gl import Config as GL
from freee_a11y_gl import process_yaml_data
#from get_yaml_data import get_yaml_data

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
        force=True  # 既存のハンドラを上書き
    )

def main() -> None:
    # Set up initial logging with default level
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    args = parse_args()
    
    try:
        # Load configuration
        logger.debug(f"Loading configuration from {args.config if args.config else 'default locations'}")
        config = load_configuration(args.config)
        
        # Update log level from config if needed
        current_level = logging.getLogger().getEffectiveLevel()
        config_level = config.get_log_level()
        if current_level != config_level:
            logger.debug(f"Updating log level from {current_level} to {config_level}")
            setup_logging(config_level)
        
        # Log which environment we're using
        env_type = "production" if args.production else "development"
        logger.info(f"Using {env_type} environment")
        
        # Get authentication using Path objects from config
        auth_manager = GoogleAuthManager(
            credentials_path=config.credentials_path.as_posix(),
            token_path=config.token_path.as_posix()
        )
        credentials = auth_manager.get_credentials()
        
    except FileNotFoundError as e:
        logger.error(f"Authentication error: {e}")
        return
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {e}", exc_info=True)
        return

    try:
        # Get base directory using unified handler
        source_path = config.get_basedir(args.basedir)
        logger.debug(f"Using base directory: {source_path}")
            
        # Set base URL
        base_url = "https://a11y-guidelines.freee.co.jp"
        GL.set_base_url(base_url)
        logger.debug(f"Using base URL: {base_url}")
        
        source_data = process_yaml_data(str(source_path))
    except Exception as e:
        logger.error(f"Failed to load source data: {e}")
        return

    try:
        # Get appropriate spreadsheet ID
        spreadsheet_id = config.get_spreadsheet_id(args.production)
        logger.debug(f"Using spreadsheet ID: {spreadsheet_id}")
        
        # Generate checklist
        generator = ChecklistSheetGenerator(credentials, spreadsheet_id)
        generator.generate_checklist(source_data, initialize=args.init)
        logger.info(f"Checklist generation completed successfully in {env_type} environment")
        
    except Exception as e:
        logger.error(f"Failed to generate checklist: {e}", exc_info=True)
        return

if __name__ == '__main__':
    main()
