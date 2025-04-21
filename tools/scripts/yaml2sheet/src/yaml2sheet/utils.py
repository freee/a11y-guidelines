from typing import Dict, List, Any, Union
from .config import M17nField

def format_statement_summary(statement: M17nField) -> M17nField:
    """Format a check statement summary into a complete sentence
    
    Args:
        statement: Multilingual statement to format
        
    Returns:
        M17nField: Formatted statement with proper punctuation
    """
    return {
        'ja': f"{statement['ja']}ことを確認する。",
        'en': f"Verify that {statement['en']}."
    }

def l10n_string(field: Union[str, Dict[str, str], None], lang: str) -> str:
    """Get localized string from a multilingual field
    
    Args:
        field: String, multilingual field, or None
        lang: Language code to retrieve
        
    Returns:
        str: Localized string for the language, or empty string if None
    """
    if field is None:
        return ''
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        return field.get(lang, field.get('ja', ''))
    return ''

def adjust_sheet_size(sheet_id: int, required_rows: int, required_columns: int,
                     current_row_count: int, current_column_count: int) -> List[Dict]:
    """Generate requests to adjust sheet dimensions
    
    Args:
        sheet_id: ID of the sheet to modify
        required_rows: Number of rows needed
        required_columns: Number of columns needed
        current_row_count: Current number of rows
        current_column_count: Current number of columns
        
    Returns:
        List[Dict]: List of sheet size adjustment requests
    """
    requests = []
    
    # Adjust rows if needed
    if current_row_count < required_rows:
        requests.append({
            'appendDimension': {
                'sheetId': sheet_id,
                'dimension': 'ROWS',
                'length': required_rows - current_row_count
            }
        })
    elif current_row_count > required_rows:
        requests.append({
            'deleteDimension': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': required_rows,
                    'endIndex': current_row_count
                }
            }
        })
    
    # Adjust columns if needed
    if current_column_count < required_columns:
        requests.append({
            'appendDimension': {
                'sheetId': sheet_id,
                'dimension': 'COLUMNS',
                'length': required_columns - current_column_count
            }
        })
    elif current_column_count > required_columns:
        requests.append({
            'deleteDimension': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': required_columns,
                    'endIndex': current_column_count
                }
            }
        })
    
    return requests

def create_version_info_request(version: str, date: str, sheet_id: int) -> Dict:
    """Create request to update version info cell
    
    Args:
        version: Version string
        date: Version date
        sheet_id: ID of the sheet to update
        
    Returns:
        Dict: Version info update request
    """
    # A27 cell position (0-based indices)
    row_index = 26  # 27 - 1
    column_index = 0  # A = 0
    
    version_string = f"チェックリスト・バージョン：{version} ({date})"
    
    return {
        'updateCells': {
            'rows': [{
                'values': [{
                    'userEnteredValue': {
                        'stringValue': version_string
                    }
                }]
            }],
            'fields': 'userEnteredValue',
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': row_index,
                'endRowIndex': row_index + 1,
                'startColumnIndex': column_index,
                'endColumnIndex': column_index + 1
            }
        }
    }
