"""Spreadsheet management for yaml2sheet."""

import logging
from typing import Dict, List, Any, Optional
from .sheet_api_client import SheetsAPIClient

logger = logging.getLogger(__name__)

class SpreadsheetManager:
    """Manages spreadsheet structure and existing sheets"""
    
    def __init__(self, api_client: SheetsAPIClient):
        """Initialize the spreadsheet manager
        
        Args:
            api_client: Google Sheets API client
        """
        self.api_client = api_client
        self.existing_sheets: Dict[str, Dict[str, Any]] = {}
        self.protected_ranges: Dict[int, List[int]] = {}
        self._sheets_loaded = False

    def _load_existing_sheets(self) -> None:
        """Load existing sheet information including protected ranges from spreadsheet"""
        try:
            # スプレッドシートの基本情報を取得
            spreadsheet = self.api_client.get_spreadsheet_info()

            logger.debug("Loading existing sheets")            
            self.existing_sheets = {}
            self.protected_ranges = {}  # 保護範囲情報を格納する辞書
            
            for sheet in spreadsheet.get('sheets', []):
                properties = sheet['properties']
                title = properties['title']
                sheet_id = properties['sheetId']
                logger.debug(f"Found existing sheet: '{title}'")
                self.existing_sheets[title] = {
                    'sheetId': sheet_id,
                    'index': properties.get('index', 0)
                }
                
                # 保護範囲情報があれば取得
                if 'protectedRanges' in sheet:
                    self.protected_ranges[sheet_id] = [
                        protected_range.get('protectedRangeId')
                        for protected_range in sheet.get('protectedRanges', [])
                        if 'protectedRangeId' in protected_range
                    ]
                    if self.protected_ranges[sheet_id]:
                        logger.debug(f"Found {len(self.protected_ranges[sheet_id])} protected ranges in sheet '{title}'")
            
            logger.debug(f"Loaded existing sheets: {list(self.existing_sheets.keys())}")
            
            # 保護範囲の詳細情報を取得
            if any(self.protected_ranges.values()):
                try:
                    # 保護範囲の詳細情報を取得するには別のAPI呼び出しが必要
                    protected_ranges_response = self.api_client.get_by_data_filter([
                        {"developerMetadataLookup": {"metadataKey": "protectedRanges"}}
                    ])
                    
                    # 追加の処理が必要であれば、ここに書く
                    # 必要に応じて protected_ranges_response からさらに詳細情報を抽出
                    
                except Exception as e:
                    # 詳細情報の取得に失敗してもプログラムを続行する
                    logger.warning(f"Failed to get detailed protected ranges info: {e}")
        except Exception as e:
            logger.error(f"Error loading existing sheets: {e}")
            raise

    def initialize_spreadsheet(self) -> None:
        """Initialize spreadsheet by removing extra sheets"""
        try:
            spreadsheet = self.api_client.get_spreadsheet_info()
            
            # Delete sheets after first
            if len(spreadsheet.get('sheets', [])) > 1:
                delete_requests = [
                    {'deleteSheet': {'sheetId': sheet['properties']['sheetId']}}
                    for sheet in spreadsheet['sheets'][1:]
                ]
                
                if delete_requests:
                    self.api_client.batch_update(delete_requests)
                    logger.info("Deleted existing sheets except the first one")
            
            # Reset existing sheets info
            self.existing_sheets = {
                spreadsheet['sheets'][0]['properties']['title']: {
                    'sheetId': spreadsheet['sheets'][0]['properties']['sheetId'],
                    'index': 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error initializing spreadsheet: {e}")
            raise

    def _ensure_sheets_loaded(self) -> None:
        """Ensure existing sheets are loaded"""
        if not self._sheets_loaded:
            self._load_existing_sheets()
            self._sheets_loaded = True

    def get_sheet_id(self, sheet_name: str) -> Optional[int]:
        """Get sheet ID by name
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            Optional[int]: Sheet ID if found, None otherwise
        """
        self._ensure_sheets_loaded()
        sheet_info = self.existing_sheets.get(sheet_name)
        return sheet_info['sheetId'] if sheet_info else None

    def sheet_exists(self, sheet_name: str) -> bool:
        """Check if sheet exists
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            bool: True if sheet exists
        """
        self._ensure_sheets_loaded()
        return sheet_name in self.existing_sheets

    def get_first_sheet_id(self) -> int:
        """Get ID of first sheet
        
        Returns:
            int: Sheet ID
            
        Raises:
            KeyError: If no sheets exist
        """
        self._ensure_sheets_loaded()
        first_sheet_name = next(iter(self.existing_sheets))
        return self.existing_sheets[first_sheet_name]['sheetId']

    def update_sheet_info(self, sheet_name: str, sheet_id: int, index: int = 0) -> None:
        """Update sheet information after creation
        
        Args:
            sheet_name: Name of the sheet
            sheet_id: ID of the sheet
            index: Index of the sheet
        """
        self.existing_sheets[sheet_name] = {
            'sheetId': sheet_id,
            'index': index
        }

    def get_protected_ranges(self, sheet_id: int) -> List[int]:
        """Get protected range IDs for a sheet
        
        Args:
            sheet_id: ID of the sheet
            
        Returns:
            List[int]: List of protected range IDs
        """
        return self.protected_ranges.get(sheet_id, [])

    def get_sheet_grid_properties(self, sheet_name: str) -> Optional[Dict[str, Any]]:
        """Get grid properties for a sheet
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            Optional[Dict[str, Any]]: Grid properties if found
        """
        try:
            spreadsheet = self.api_client.get_spreadsheet_with_ranges([sheet_name])
            
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['gridProperties']
            return None
        except Exception as e:
            logger.error(f"Error getting grid properties for sheet '{sheet_name}': {e}")
            return None
