import os
import json
import logging
from auth import GoogleAuthManager
from sheet_generator import ChecklistSheetGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Config
SPREADSHEET_ID = os.getenv('CHECKSHEET_ID')
SOURCE_FILE = 'checks-v5.json'

def main():
    try:
        # Get authentication
        auth_manager = GoogleAuthManager()
        credentials = auth_manager.get_credentials()
        
    except FileNotFoundError as e:
        logger.error(f"Authentication error: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        return

    try:
        # Load source data
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load source data: {e}")
        return

    try:
        # Generate checklist
        generator = ChecklistSheetGenerator(credentials, SPREADSHEET_ID)
        generator.generate_checklist(source_data, initialize=False)
        logger.info("Checklist generation completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to generate checklist: {e}")
        return

if __name__ == '__main__':
    main()
