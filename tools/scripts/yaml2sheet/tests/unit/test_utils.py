"""
Tests for utils module.

Tests utility functions for formatting, localization, and Google Sheets operations.
"""

import pytest
from yaml2sheet.utils import (
    format_statement_summary,
    l10n_string,
    adjust_sheet_size,
    create_version_info_request,
    get_generated_data_start_column,
    get_generated_data_end_column,
    get_result_column_index,
    get_calculated_result_column_index,
    column_index_to_letter,
    has_generated_data
)


class TestFormatStatementSummary:
    """Test format_statement_summary function."""
    
    def test_format_statement_summary_basic(self):
        """Test basic statement formatting."""
        statement = {
            'ja': 'テストが正しく動作する',
            'en': 'the test works correctly'
        }
        
        result = format_statement_summary(statement)
        
        expected = {
            'ja': 'テストが正しく動作することを確認する。',
            'en': 'Verify that the test works correctly.'
        }
        assert result == expected
    
    def test_format_statement_summary_empty_strings(self):
        """Test statement formatting with empty strings."""
        statement = {
            'ja': '',
            'en': ''
        }
        
        result = format_statement_summary(statement)
        
        expected = {
            'ja': 'ことを確認する。',
            'en': 'Verify that .'
        }
        assert result == expected
    
    def test_format_statement_summary_with_punctuation(self):
        """Test statement formatting when input already has punctuation."""
        statement = {
            'ja': 'フォームが適切に送信される。',
            'en': 'the form submits properly.'
        }
        
        result = format_statement_summary(statement)
        
        expected = {
            'ja': 'フォームが適切に送信される。ことを確認する。',
            'en': 'Verify that the form submits properly..'
        }
        assert result == expected
    
    def test_format_statement_summary_unicode_characters(self):
        """Test statement formatting with unicode characters."""
        statement = {
            'ja': 'ユーザーが正常にログインできる',
            'en': 'users can log in successfully'
        }
        
        result = format_statement_summary(statement)
        
        expected = {
            'ja': 'ユーザーが正常にログインできることを確認する。',
            'en': 'Verify that users can log in successfully.'
        }
        assert result == expected


class TestL10nString:
    """Test l10n_string function."""
    
    def test_l10n_string_with_dict_ja(self):
        """Test localization with dictionary and Japanese language."""
        field = {
            'ja': '日本語テキスト',
            'en': 'English text'
        }
        
        result = l10n_string(field, 'ja')
        assert result == '日本語テキスト'
    
    def test_l10n_string_with_dict_en(self):
        """Test localization with dictionary and English language."""
        field = {
            'ja': '日本語テキスト',
            'en': 'English text'
        }
        
        result = l10n_string(field, 'en')
        assert result == 'English text'
    
    def test_l10n_string_with_dict_missing_language(self):
        """Test localization with dictionary missing requested language."""
        field = {
            'ja': '日本語テキスト',
            'en': 'English text'
        }
        
        result = l10n_string(field, 'fr')
        assert result == '日本語テキスト'  # Falls back to 'ja'
    
    def test_l10n_string_with_dict_missing_ja_fallback(self):
        """Test localization with dictionary missing both requested and 'ja' languages."""
        field = {
            'en': 'English text',
            'de': 'German text'
        }
        
        result = l10n_string(field, 'fr')
        assert result == ''  # No 'ja' fallback available
    
    def test_l10n_string_with_dict_empty_values(self):
        """Test localization with dictionary containing empty values."""
        field = {
            'ja': '',
            'en': 'English text'
        }
        
        result = l10n_string(field, 'ja')
        assert result == ''
    
    def test_l10n_string_with_string(self):
        """Test localization with plain string input."""
        field = "Plain string"
        
        result = l10n_string(field, 'ja')
        assert result == "Plain string"
        
        result = l10n_string(field, 'en')
        assert result == "Plain string"
    
    def test_l10n_string_with_none(self):
        """Test localization with None input."""
        result = l10n_string(None, 'ja')
        assert result == ''
        
        result = l10n_string(None, 'en')
        assert result == ''
    
    def test_l10n_string_with_empty_dict(self):
        """Test localization with empty dictionary."""
        field = {}
        
        result = l10n_string(field, 'ja')
        assert result == ''
        
        result = l10n_string(field, 'en')
        assert result == ''
    
    def test_l10n_string_with_non_string_dict_values(self):
        """Test localization with non-string values in dictionary."""
        field = {
            'ja': 123,
            'en': ['list', 'value']
        }
        
        result = l10n_string(field, 'ja')
        assert result == 123
        
        result = l10n_string(field, 'en')
        assert result == ['list', 'value']

    def test_l10n_string_with_invalid_type(self):
        """Test localization with invalid field type (not None, str, or dict)."""
        # Test with integer
        result = l10n_string(123, 'ja')
        assert result == ''
        
        # Test with list
        result = l10n_string(['item1', 'item2'], 'en')
        assert result == ''
        
        # Test with boolean
        result = l10n_string(True, 'ja')
        assert result == ''


class TestAdjustSheetSize:
    """Test adjust_sheet_size function."""
    
    def test_adjust_sheet_size_no_changes_needed(self):
        """Test when no size adjustments are needed."""
        requests = adjust_sheet_size(
            sheet_id=123,
            required_rows=100,
            required_columns=26,
            current_row_count=100,
            current_column_count=26
        )
        
        assert requests == []
    
    def test_adjust_sheet_size_add_rows(self):
        """Test adding rows when more are needed."""
        requests = adjust_sheet_size(
            sheet_id=123,
            required_rows=150,
            required_columns=26,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'appendDimension': {
                    'sheetId': 123,
                    'dimension': 'ROWS',
                    'length': 50
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_remove_rows(self):
        """Test removing rows when fewer are needed."""
        requests = adjust_sheet_size(
            sheet_id=123,
            required_rows=80,
            required_columns=26,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 123,
                        'dimension': 'ROWS',
                        'startIndex': 80,
                        'endIndex': 100
                    }
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_add_columns(self):
        """Test adding columns when more are needed."""
        requests = adjust_sheet_size(
            sheet_id=123,
            required_rows=100,
            required_columns=30,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'appendDimension': {
                    'sheetId': 123,
                    'dimension': 'COLUMNS',
                    'length': 4
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_remove_columns(self):
        """Test removing columns when fewer are needed."""
        requests = adjust_sheet_size(
            sheet_id=123,
            required_rows=100,
            required_columns=20,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 123,
                        'dimension': 'COLUMNS',
                        'startIndex': 20,
                        'endIndex': 26
                    }
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_add_both_dimensions(self):
        """Test adding both rows and columns."""
        requests = adjust_sheet_size(
            sheet_id=456,
            required_rows=120,
            required_columns=30,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'appendDimension': {
                    'sheetId': 456,
                    'dimension': 'ROWS',
                    'length': 20
                }
            },
            {
                'appendDimension': {
                    'sheetId': 456,
                    'dimension': 'COLUMNS',
                    'length': 4
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_remove_both_dimensions(self):
        """Test removing both rows and columns."""
        requests = adjust_sheet_size(
            sheet_id=789,
            required_rows=80,
            required_columns=20,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 789,
                        'dimension': 'ROWS',
                        'startIndex': 80,
                        'endIndex': 100
                    }
                }
            },
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 789,
                        'dimension': 'COLUMNS',
                        'startIndex': 20,
                        'endIndex': 26
                    }
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_mixed_operations(self):
        """Test mixed operations (add rows, remove columns)."""
        requests = adjust_sheet_size(
            sheet_id=999,
            required_rows=150,
            required_columns=20,
            current_row_count=100,
            current_column_count=26
        )
        
        expected = [
            {
                'appendDimension': {
                    'sheetId': 999,
                    'dimension': 'ROWS',
                    'length': 50
                }
            },
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 999,
                        'dimension': 'COLUMNS',
                        'startIndex': 20,
                        'endIndex': 26
                    }
                }
            }
        ]
        assert requests == expected
    
    def test_adjust_sheet_size_zero_dimensions(self):
        """Test with zero required dimensions."""
        requests = adjust_sheet_size(
            sheet_id=111,
            required_rows=0,
            required_columns=0,
            current_row_count=10,
            current_column_count=10
        )
        
        expected = [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 111,
                        'dimension': 'ROWS',
                        'startIndex': 0,
                        'endIndex': 10
                    }
                }
            },
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': 111,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 10
                    }
                }
            }
        ]
        assert requests == expected


class TestCreateVersionInfoRequest:
    """Test create_version_info_request function."""
    
    def test_create_version_info_request_basic(self):
        """Test basic version info request creation with default parameters."""
        request = create_version_info_request("1.0.0", "2024-01-01", 123)
        
        expected = {
            'updateCells': {
                'rows': [{
                    'values': [{
                        'userEnteredValue': {
                            'stringValue': 'チェックリスト・バージョン：1.0.0 (2024-01-01)'
                        }
                    }]
                }],
                'fields': 'userEnteredValue',
                'range': {
                    'sheetId': 123,
                    'startRowIndex': 26,  # A27 (0-based)
                    'endRowIndex': 27,
                    'startColumnIndex': 0,  # Column A
                    'endColumnIndex': 1
                }
            }
        }
        assert request == expected

    def test_create_version_info_request_custom_position(self):
        """Test version info request creation with custom cell position."""
        # Test B15 position (row_index=14, column_index=1)
        request = create_version_info_request("2.0.0", "2024-02-01", 456, 
                                            row_index=14, column_index=1)
        
        expected = {
            'updateCells': {
                'rows': [{
                    'values': [{
                        'userEnteredValue': {
                            'stringValue': 'チェックリスト・バージョン：2.0.0 (2024-02-01)'
                        }
                    }]
                }],
                'fields': 'userEnteredValue',
                'range': {
                    'sheetId': 456,
                    'startRowIndex': 14,  # B15 (0-based)
                    'endRowIndex': 15,
                    'startColumnIndex': 1,  # Column B
                    'endColumnIndex': 2
                }
            }
        }
        assert request == expected

    def test_create_version_info_request_different_positions(self):
        """Test version info request with various cell positions."""
        test_cases = [
            # (row_index, column_index, description)
            (0, 0, "A1"),
            (9, 25, "Z10"),
            (99, 26, "AA100"),
        ]
        
        for row_idx, col_idx, description in test_cases:
            request = create_version_info_request("1.0", "2024-01-01", 123,
                                                row_index=row_idx, column_index=col_idx)
            
            range_info = request['updateCells']['range']
            assert range_info['startRowIndex'] == row_idx, f"Failed for {description}"
            assert range_info['endRowIndex'] == row_idx + 1, f"Failed for {description}"
            assert range_info['startColumnIndex'] == col_idx, f"Failed for {description}"
            assert range_info['endColumnIndex'] == col_idx + 1, f"Failed for {description}"
    
    def test_create_version_info_request_empty_version(self):
        """Test version info request with empty version."""
        request = create_version_info_request("", "", 456)
        
        expected = {
            'updateCells': {
                'rows': [{
                    'values': [{
                        'userEnteredValue': {
                            'stringValue': 'チェックリスト・バージョン： ()'
                        }
                    }]
                }],
                'fields': 'userEnteredValue',
                'range': {
                    'sheetId': 456,
                    'startRowIndex': 26,
                    'endRowIndex': 27,
                    'startColumnIndex': 0,
                    'endColumnIndex': 1
                }
            }
        }
        assert request == expected
    
    def test_create_version_info_request_long_version(self):
        """Test version info request with long version string."""
        version = "1.2.3-beta.4+build.567"
        date = "2024-12-31T23:59:59Z"
        
        request = create_version_info_request(version, date, 789)
        
        expected_string = f"チェックリスト・バージョン：{version} ({date})"
        
        assert request['updateCells']['rows'][0]['values'][0]['userEnteredValue']['stringValue'] == expected_string
        assert request['updateCells']['range']['sheetId'] == 789
    
    def test_create_version_info_request_unicode_version(self):
        """Test version info request with unicode characters."""
        version = "バージョン1.0"
        date = "令和6年1月1日"
        
        request = create_version_info_request(version, date, 999)
        
        expected_string = f"チェックリスト・バージョン：{version} ({date})"
        
        assert request['updateCells']['rows'][0]['values'][0]['userEnteredValue']['stringValue'] == expected_string
    
    def test_create_version_info_request_cell_position(self):
        """Test that version info is placed in correct cell position (A27)."""
        request = create_version_info_request("1.0", "2024-01-01", 100)
        
        range_info = request['updateCells']['range']
        
        # A27 should be row index 26 (0-based), column index 0
        assert range_info['startRowIndex'] == 26
        assert range_info['endRowIndex'] == 27
        assert range_info['startColumnIndex'] == 0
        assert range_info['endColumnIndex'] == 1
    
    def test_create_version_info_request_different_sheet_ids(self):
        """Test version info request with different sheet IDs."""
        sheet_ids = [0, 1, 999, 123456]
        
        for sheet_id in sheet_ids:
            request = create_version_info_request("1.0", "2024-01-01", sheet_id)
            assert request['updateCells']['range']['sheetId'] == sheet_id
    
    def test_create_version_info_request_fields_and_structure(self):
        """Test that the request has correct fields and structure."""
        request = create_version_info_request("1.0", "2024-01-01", 123)
        
        # Check top-level structure
        assert 'updateCells' in request
        update_cells = request['updateCells']
        
        # Check required fields
        assert 'rows' in update_cells
        assert 'fields' in update_cells
        assert 'range' in update_cells
        
        # Check fields value
        assert update_cells['fields'] == 'userEnteredValue'
        
        # Check rows structure
        assert len(update_cells['rows']) == 1
        assert 'values' in update_cells['rows'][0]
        assert len(update_cells['rows'][0]['values']) == 1
        assert 'userEnteredValue' in update_cells['rows'][0]['values'][0]
        assert 'stringValue' in update_cells['rows'][0]['values'][0]['userEnteredValue']
