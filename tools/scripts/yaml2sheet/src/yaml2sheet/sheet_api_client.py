"""Google Sheets API client for yaml2sheet."""

import logging
from typing import Dict, List, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class SheetsAPIClient:
    """Handles Google Sheets API communication"""
    
    def __init__(self, credentials: Credentials, spreadsheet_id: str):
        """Initialize the API client
        
        Args:
            credentials: Google API credentials
            spreadsheet_id: Target spreadsheet ID
        """
        # Import build from sheet_generator for backward compatibility with tests
        try:
            from . import sheet_generator
            build_func = sheet_generator.build
        except (ImportError, AttributeError):
            build_func = build
            
        self.service = build_func('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id

    def get_spreadsheet_info(self) -> Dict[str, Any]:
        """Get spreadsheet information
        
        Returns:
            Dict[str, Any]: Spreadsheet information
        """
        return self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id
        ).execute()

    def get_spreadsheet_with_ranges(self, ranges: List[str]) -> Dict[str, Any]:
        """Get spreadsheet information with specific ranges
        
        Args:
            ranges: List of ranges to include
            
        Returns:
            Dict[str, Any]: Spreadsheet information
        """
        return self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id,
            ranges=ranges,
            includeGridData=False
        ).execute()

    def batch_update(self, requests: List[Dict]) -> Dict[str, Any]:
        """Execute batch update requests
        
        Args:
            requests: List of update requests
            
        Returns:
            Dict[str, Any]: API response
        """
        return self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={'requests': requests}
        ).execute()

    def get_by_data_filter(self, data_filters: List[Dict]) -> Dict[str, Any]:
        """Get spreadsheet data by filter
        
        Args:
            data_filters: List of data filters
            
        Returns:
            Dict[str, Any]: Filtered data
        """
        return self.service.spreadsheets().getByDataFilter(
            spreadsheetId=self.spreadsheet_id,
            body={"dataFilters": data_filters}
        ).execute()
