from typing import Dict, List, Optional
import logging
from .sheet_structure import SheetStructure
from .config import CHECK_RESULTS, FINAL_CHECK_RESULTS, COLUMNS
from .utils import get_generated_data_start_column, get_generated_data_end_column, get_result_column_index, has_generated_data

logger = logging.getLogger(__name__)

class SheetFormatter:
    """Handles sheet formatting operations including conditional formatting and protection"""
    
    def __init__(self, current_lang: str, current_target: str, editor_email: str = ""):
        self.current_lang = current_lang
        self.current_target = current_target
        self.editor_email = editor_email

    def apply_basic_formatting(self, sheet_id: int, data_length: int) -> List[Dict]:
        """Apply basic sheet formatting
        
        Args:
            sheet_id: ID of sheet to format
            data_length: Number of data rows
            
        Returns:
            List[Dict]: List of formatting requests
        """
        requests = []
        
        # Header row formatting
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                        'textFormat': {'bold': True},
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment,wrapStrategy)'
            }
        })

        # Set wrapStrategy to all data cells.
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': data_length + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat.wrapStrategy'
            }
        })

        # Freeze top row
        requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        })
        
        return requests
        
    def add_conditional_formatting(self, sheet_id: int, data_length: int) -> List[Dict]:
        """Add conditional formatting rules
        
        Args:
            sheet_id: ID of sheet to format
            data_length: Number of data rows
            
        Returns:
            List[Dict]: List of conditional formatting requests
        """
        result_column = self.get_result_column_index()
        requests = []
        
        # Pass condition formatting for user-entered check results
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': data_length + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['pass'][self.current_lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}
                        }
                    }
                }
            }
        })
        
        # Fail condition formatting  for user-entered check results
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': data_length + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['fail'][self.current_lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.96, 'green': 0.80, 'blue': 0.80}
                        }
                    }
                }
            }
        })

        # Add conditoinal formatting if there are generated data columns
        if has_generated_data(self.current_target):
            generated_column_start = get_generated_data_start_column() + 1
            generated_column_end = get_generated_data_end_column(self.current_target)
            # Pass condition formatting for generated check results
            requests.append({
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'endRowIndex': data_length + 1,
                            'startColumnIndex': generated_column_start,
                            'endColumnIndex': generated_column_end
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{'userEnteredValue': FINAL_CHECK_RESULTS['pass'][self.current_lang]}]
                            },
                            'format': {
                                'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}
                            }
                        }
                    }
                }
            })
            
            # Fail condition formatting for generated check results
            requests.append({
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'endRowIndex': data_length + 1,
                            'startColumnIndex': generated_column_start,
                            'endColumnIndex': generated_column_end
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{'userEnteredValue': FINAL_CHECK_RESULTS['fail'][self.current_lang]}]
                            },
                            'format': {
                                'backgroundColor': {'red': 0.96, 'green': 0.80, 'blue': 0.80}
                            }
                        }
                    }
                }
            })
        return requests
        
    def get_result_column_index(self) -> int:
        """Get index of result column based on current target
        
        Returns:
            int: Index of result column
        """
        return get_result_column_index(self.current_target)

    def add_protection_settings(self, sheet_id: int, sheet: SheetStructure) -> List[Dict]:
        """Add sheet protection settings
        
        Args:
            sheet_id: ID of sheet to protect
            sheet: Sheet structure containing protection settings
            
        Returns:
            List[Dict]: List of protection requests
        """
        requests = []
        data_length = len(sheet.data)
        
        # Protect generated data columns if present
        if has_generated_data(self.current_target):
            generated_data_start = get_generated_data_start_column()
            generated_data_count = len(COLUMNS[self.current_target]['generatedData'])
            
            protection_request = {
                'addProtectedRange': {
                    'protectedRange': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'endRowIndex': data_length + 1,
                            'startColumnIndex': generated_data_start,
                            'endColumnIndex': generated_data_start + generated_data_count
                        },
                        'description': 'Generated data protection',
                        'warningOnly': False,
                        'editors': {
                            'domainUsersCanEdit': False
                        }
                    }
                }
            }
            if self.editor_email:
                protection_request['addProtectedRange']['protectedRange']['editors']['users'] = [self.editor_email]
            requests.append(protection_request)
        return requests

    def protect_parent_check_cells(self, sheet_id: int, row_index: int) -> Dict:
        """Protect parent check cells that have subchecks
        
        Args:
            sheet_id: Sheet ID
            row_index: Row index (0-based)
            
        Returns:
            Dict: Protection request
        """
        result_column = self.get_result_column_index()
        
        protection_request = {
            'addProtectedRange': {
                'protectedRange': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_index,
                        'endRowIndex': row_index + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    },
                    'description': 'Parent check cell protection',
                    'warningOnly': False,
                    'editors': {
                        'domainUsersCanEdit': False
                    }
                }
            }
        }
        if self.editor_email:
            protection_request['addProtectedRange']['protectedRange']['editors']['users'] = [self.editor_email]
        return protection_request
