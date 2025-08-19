from typing import Dict, List, Union
from .config import M17nField, COLUMNS


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


def adjust_sheet_size(sheet_id: int, required_rows: int,
                      required_columns: int, current_row_count: int,
                      current_column_count: int) -> List[Dict]:
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


def create_version_info_request(version: str, date: str, sheet_id: int,
                                row_index: int = 26,
                                column_index: int = 0) -> Dict:
    """Create request to update version info cell

    Args:
        version: Version string
        date: Version date
        sheet_id: ID of the sheet to update
        row_index: Row index (0-based, default: 26 for row 27)
        column_index: Column index (0-based, default: 0 for column A)

    Returns:
        Dict: Version info update request
    """
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


def get_generated_data_start_column(target_id: str = None) -> int:
    """Get the starting column index for generated data

    Args:
        target_id: Target ID (unused, kept for consistency)

    Returns:
        int: Starting column index for generated data
    """
    return len(COLUMNS['idCols'])


def get_generated_data_end_column(target_id: str) -> int:
    """Get the ending column index for generated data

    Args:
        target_id: Target ID to get generated data length for

    Returns:
        int: Ending column index for generated data
    """
    return len(COLUMNS['idCols']) + len(COLUMNS[target_id]['generatedData'])


def get_result_column_index(target_id: str, columns_config=None) -> int:
    """Get the column index for the result column

    Args:
        target_id: Target ID to calculate result column for
        columns_config: Optional COLUMNS configuration (defaults to global
                       COLUMNS)

    Returns:
        int: Column index for the result column
    """
    # Use provided config or default to global COLUMNS
    config = columns_config if columns_config is not None else COLUMNS

    # Result column comes after idCols and generatedData
    if target_id not in config:
        # For missing target_id, assume no generated data (0 columns)
        return len(config['idCols']) + 0
    return len(config['idCols']) + len(config[target_id]['generatedData'])


def get_calculated_result_column_index(target_id: str = None) -> int:
    """Get the column index for the calculated result column

    Args:
        target_id: Target ID (unused, kept for consistency)

    Returns:
        int: Column index for the calculated result column (finalResult + 1)
    """
    return len(COLUMNS['idCols']) + 1


def column_index_to_letter(column_index: int) -> str:
    """Convert column index to Excel column letter

    Args:
        column_index: 0-based column index

    Returns:
        str: Excel column letter (A, B, C, etc.)
    """
    return chr(ord('A') + column_index)


def has_generated_data(target_id: str) -> bool:
    """Check if target has generated data columns

    Args:
        target_id: Target ID to check

    Returns:
        bool: True if target has generated data columns
    """
    return bool(COLUMNS.get(target_id, {}).get('generatedData', []))
