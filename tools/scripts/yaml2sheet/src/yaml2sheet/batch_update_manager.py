from typing import Dict, List
import logging
from .utils import create_version_info_request

logger = logging.getLogger(__name__)


class BatchUpdateManager:
    """Manages batch update operations for spreadsheet updates"""

    def __init__(self, api_client, spreadsheet_manager):
        self.api_client = api_client
        self.spreadsheet_manager = spreadsheet_manager

    def execute_batch_update(self, initial_requests: List[Dict], version_info: Dict = None) -> None:
        """Execute batch update of spreadsheet with improved chunking for timeout prevention

        Args:
            initial_requests: List of all initial requests
            version_info: Optional version information to add
        """
        try:
            # Execute sheet creation requests
            self._execute_sheet_creation_requests(initial_requests)

            # Generate and execute remaining updates
            self._execute_sheet_update_requests(initial_requests, version_info)

        except Exception as e:
            logger.error(f"Error executing batch update: {e}")
            raise

    def _execute_sheet_creation_requests(self, initial_requests: List[Dict]) -> None:
        """Execute sheet creation requests and update sheet IDs

        Args:
            initial_requests: List of all initial requests
        """
        creation_requests = [req for req in initial_requests if 'addSheet' in req]
        if not creation_requests:
            return

        sheet_titles = [req.get('addSheet', {}).get('properties', {}).get('title') for req in creation_requests]
        logger.info(f"Creating sheets: {sheet_titles}")
        creation_response = self.api_client.batch_update(creation_requests)

        # Update sheet IDs
        for reply in creation_response.get('replies', []):
            if 'addSheet' in reply:
                sheet_id = reply['addSheet']['properties']['sheetId']
                sheet_title = reply['addSheet']['properties']['title']
                self.spreadsheet_manager.update_sheet_info(sheet_title, sheet_id, 0)

    def _execute_sheet_update_requests(self, initial_requests: List[Dict], version_info: Dict = None) -> None:
        """Execute sheet update requests in batches

        Args:
            initial_requests: List of all initial requests
            version_info: Optional version information to add
        """
        update_requests = [req for req in initial_requests if 'addSheet' not in req]

        if not update_requests:
            return

        # Add version info request if provided
        if version_info:
            self._add_version_info_request(update_requests, version_info)

        # Process in smaller batches to avoid timeouts
        self._process_update_batches(update_requests)

    def _add_version_info_request(self, update_requests: List[Dict], version_info: Dict) -> None:
        """Add version info request if version info is available

        Args:
            update_requests: List of update requests to append to
            version_info: Version information containing 'version' and 'date'
        """
        first_sheet_id = self.spreadsheet_manager.get_first_sheet_id()
        version_update_request = create_version_info_request(
            version_info['version'],
            version_info['date'],
            first_sheet_id
        )
        update_requests.append(version_update_request)

    def _process_update_batches(self, update_requests: List[Dict]) -> None:
        """Process update requests in batches to avoid timeouts

        Args:
            update_requests: List of update requests to process
        """
        BATCH_SIZE = 50  # Reduced batch size to avoid timeout
        total_requests = len(update_requests)
        logger.info(f"Updating {total_requests} sheet contents in smaller batches")

        # Process in batches to avoid timeout
        for i in range(0, total_requests, BATCH_SIZE):
            end_idx = min(i + BATCH_SIZE, total_requests)
            batch = update_requests[i:end_idx]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (total_requests - 1) // BATCH_SIZE + 1

            batch_info = f"Processing batch {batch_num}/{total_batches}: requests {i+1}-{end_idx} of {total_requests}"
            logger.info(batch_info)

            try:
                # Execute batch with longer timeout setting
                self.api_client.batch_update(batch)
                logger.info(f"Batch {batch_num} completed successfully")
            except Exception as e:
                logger.error(f"Error in batch {batch_num}: {e}")
                # Continue with next batch even if one fails

        logger.info("All sheet updates completed")
