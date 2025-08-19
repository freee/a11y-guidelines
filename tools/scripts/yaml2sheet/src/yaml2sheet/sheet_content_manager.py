from typing import Dict, List, Any
import logging
from .sheet_structure import SheetStructure
from .cell_data import CellData
from .sheet_formatter import SheetFormatter
from .column_manager import ColumnManager
from .config import COLUMNS
from .utils import adjust_sheet_size

logger = logging.getLogger(__name__)

class SheetContentManager:
    """Manages sheet content updates and formatting"""
    
    def __init__(self, api_client, spreadsheet_manager, current_lang: str, current_target: str, editor_email: str = ""):
        self.api_client = api_client
        self.spreadsheet_manager = spreadsheet_manager
        self.current_lang = current_lang
        self.current_target = current_target
        self.editor_email = editor_email
        self.column_manager = ColumnManager(current_target)
    
    def add_sheet_content_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        sheet_name: str,
        sheet: SheetStructure
    ) -> None:
        """Add requests to update sheet content and formatting
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            sheet_name: Name of the sheet
            sheet: Sheet structure containing data and format info
        """
        try:
            data_length = len(sheet.data)
            column_count = len(sheet.data[0]) if sheet.data else 26

            # Get current sheet properties and adjust size if needed
            self._adjust_sheet_size(sheet_id, sheet_name, data_length, column_count)
            
            # Clear existing content
            self._add_clear_content_request(requests, sheet_id, data_length, column_count)
            
            # Add new data in chunks
            self._add_data_update_requests(requests, sheet_id, sheet.data)
            
            # Set column widths
            self._add_column_width_requests(requests, sheet_id)
            
            # Add formatting and protection
            self._add_formatting_requests(requests, sheet_id, sheet, data_length)
            
            # Configure column visibility
            self._add_column_visibility_requests(requests, sheet_id, sheet.data, column_count)

        except Exception as e:
            logger.error(f"Error processing sheet content: {e}")
            raise

    def _adjust_sheet_size(self, sheet_id: int, sheet_name: str, data_length: int, column_count: int) -> None:
        """Adjust sheet size if needed"""
        grid_properties = self.spreadsheet_manager.get_sheet_grid_properties(sheet_name)
                
        if grid_properties:
            current_rows = grid_properties.get('rowCount', 1000)
            current_cols = grid_properties.get('columnCount', 26)
            
            size_requests = adjust_sheet_size(
                sheet_id, data_length, column_count, 
                current_rows, current_cols
            )
            
            if size_requests:
                logger.debug("Executing size adjustment requests")
                self.api_client.batch_update(size_requests)

    def _add_clear_content_request(
        self,
        requests: List[Dict],
        sheet_id: int,
        data_length: int,
        column_count: int
    ) -> None:
        """Add request to clear existing content and remove protected ranges
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            data_length: Number of data rows
            column_count: Number of columns
        """
        # Remove existing protected ranges
        if hasattr(self.spreadsheet_manager, 'protected_ranges') and sheet_id in self.spreadsheet_manager.protected_ranges:
            for protected_range_id in self.spreadsheet_manager.protected_ranges.get(sheet_id, []):
                requests.append({
                    'deleteProtectedRange': {
                        'protectedRangeId': protected_range_id
                    }
                })
            logger.debug(f"Added requests to delete {len(self.spreadsheet_manager.protected_ranges.get(sheet_id, []))} protected ranges from sheet {sheet_id}")
        
        # Clear existing cell content
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': data_length,
                    'startColumnIndex': 0,
                    'endColumnIndex': column_count
                },
                'fields': '*'
            }
        })

    def _add_data_update_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        data: List[List[CellData]]
    ) -> None:
        """Add requests to update sheet data in chunks with improved batching
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            data: Data to update
        """
        # Use smaller chunks for better reliability
        CHUNK_SIZE = 100  # Reduced from 1000 to avoid timeouts
        
        total_rows = len(data)
        logger.debug(f"Adding data update requests for {total_rows} rows in chunks of {CHUNK_SIZE}")
        
        for i in range(0, total_rows, CHUNK_SIZE):
            chunk = data[i:i + CHUNK_SIZE]
            end_idx = min(i + CHUNK_SIZE, total_rows)
            logger.debug(f"Processing rows {i+1}-{end_idx} of {total_rows}")
            
            requests.append({
                'updateCells': {
                    'rows': [
                        {'values': [cell.to_sheets_value() for cell in row]}
                        for row in chunk
                    ],
                    'fields': 'userEnteredValue,userEnteredFormat,textFormatRuns,dataValidation',
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': i,
                        'startColumnIndex': 0
                    }
                }
            })

    def _add_column_width_requests(self, requests: List[Dict], sheet_id: int) -> None:
        """Add requests to set column widths"""
        for i, width in enumerate(self.column_manager.get_column_widths()):
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': i,
                        'endIndex': i + 1
                    },
                    'properties': {'pixelSize': width},
                    'fields': 'pixelSize'
                }
            })

    def _add_formatting_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        sheet: SheetStructure,
        data_length: int
    ) -> None:
        """Add formatting and protection requests"""
        formatter = SheetFormatter(self.current_lang, self.current_target, self.editor_email)
        
        # Basic formatting
        requests.extend(formatter.apply_basic_formatting(sheet_id, data_length))
        
        # Protection settings
        requests.extend(formatter.add_protection_settings(sheet_id, sheet))
        
        # Parent check protection
        for i, row in enumerate(sheet.data[1:], start=1):
            if self._is_parent_check_with_subchecks(row):
                requests.append(formatter.protect_parent_check_cells(sheet_id, i))

    def _add_column_visibility_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        data: List[List[CellData]],
        column_count: int
    ) -> None:
        """Add requests to configure column visibility"""
        # Reset all column visibility
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': column_count
                },
                'properties': {'hiddenByUser': False},
                'fields': 'hiddenByUser'
            }
        })
        
        has_generated_data = self.column_manager.has_generated_data()
        has_subchecks = any(row[1].value for row in data[1:])  # Check B column after header
        
        if has_generated_data:
            if not has_subchecks:
                # Hide columns B-D if no subchecks
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 1,
                            'endIndex': 4
                        },
                        'properties': {'hiddenByUser': True},
                        'fields': 'hiddenByUser'
                    }
                })
            else:
                # Hide column C and merge A-B for subchecks
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 2,
                            'endIndex': 3
                        },
                        'properties': {'hiddenByUser': True},
                        'fields': 'hiddenByUser'
                    }
                })
                
                requests.append({
                    'mergeCells': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 2
                        },
                        'mergeType': 'MERGE_ALL'
                    }
                })
        else:
            # Hide column B if no generated data
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 1,
                        'endIndex': 2
                    },
                    'properties': {'hiddenByUser': True},
                    'fields': 'hiddenByUser'
                }
            })

    def _is_parent_check_with_subchecks(self, row: List[CellData]) -> bool:
        """Check if the row represents a parent check that has subchecks
        
        Args:
            row: Row data
            
        Returns:
            bool: True if this is a parent check with subchecks
        """
        # Get checkId
        check_id = row[0].value if row[0].value else ""
        
        # This would need access to data_processor.check_info
        # For now, we'll use a simpler heuristic based on the row data
        # In a full implementation, this should be injected or accessed differently
        return False  # Simplified for now - this logic should be moved or refactored
