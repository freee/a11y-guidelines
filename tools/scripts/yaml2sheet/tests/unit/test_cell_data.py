"""
Tests for cell_data module.

Tests the CellData class and CellType enum for Google Sheets cell representation.
"""

import pytest
from yaml2sheet.cell_data import CellData, CellType


class TestCellType:
    """Test CellType enumeration."""
    
    def test_cell_type_values(self):
        """Test that CellType enum has expected values."""
        assert CellType.PLAIN.value == "plain"
        assert CellType.RICH_TEXT.value == "rich_text"
        assert CellType.FORMULA.value == "formula"
    
    def test_cell_type_members(self):
        """Test that all expected CellType members exist."""
        expected_members = {'PLAIN', 'RICH_TEXT', 'FORMULA'}
        actual_members = {member.name for member in CellType}
        assert actual_members == expected_members


class TestCellData:
    """Test CellData class functionality."""
    
    def test_init_basic(self):
        """Test basic CellData initialization."""
        cell = CellData("test", CellType.PLAIN)
        
        assert cell.value == "test"
        assert cell.type == CellType.PLAIN
        assert cell.formatting is None
        assert cell.validation is None
        assert cell.protection is False
        assert cell.note is None
    
    def test_init_with_all_parameters(self):
        """Test CellData initialization with all parameters."""
        formatting = {"textFormat": {"bold": True}}
        validation = {"condition": {"type": "ONE_OF_LIST"}}
        
        cell = CellData(
            value="test",
            type=CellType.PLAIN,
            formatting=formatting,
            validation=validation,
            protection=True,
            note="Test note"
        )
        
        assert cell.value == "test"
        assert cell.type == CellType.PLAIN
        assert cell.formatting == formatting
        assert cell.validation == validation
        assert cell.protection is True
        assert cell.note == "Test note"
    
    def test_init_empty_string_plain_type(self):
        """Test that empty strings are converted to None for PLAIN type."""
        cell = CellData("", CellType.PLAIN)
        assert cell.value is None
        assert cell.formatting is None
    
    def test_init_whitespace_string_plain_type(self):
        """Test that whitespace-only strings are converted to None for PLAIN type."""
        cell = CellData("   \n\t  ", CellType.PLAIN)
        assert cell.value is None
        assert cell.formatting is None
    
    def test_init_empty_string_non_plain_type(self):
        """Test that empty strings are preserved for non-PLAIN types."""
        cell = CellData("", CellType.FORMULA)
        assert cell.value == ""
        assert cell.formatting is None
    
    def test_init_none_value(self):
        """Test initialization with None value."""
        formatting = {"textFormat": {"bold": True}}
        cell = CellData(None, CellType.PLAIN, formatting=formatting)
        
        assert cell.value is None
        assert cell.formatting is None  # Formatting should be None for None values
    
    def test_init_non_string_value(self):
        """Test initialization with non-string values."""
        cell = CellData(42, CellType.PLAIN)
        assert cell.value == 42
        assert cell.formatting is None
    
    def test_to_sheets_value_plain_type(self):
        """Test conversion to Sheets format for PLAIN type."""
        cell = CellData("test value", CellType.PLAIN)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "test value"}
        }
        assert result == expected
    
    def test_to_sheets_value_plain_type_with_formatting(self):
        """Test conversion to Sheets format for PLAIN type with formatting."""
        formatting = {"textFormat": {"bold": True}}
        cell = CellData("test", CellType.PLAIN, formatting=formatting)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "test"},
            "userEnteredFormat": formatting
        }
        assert result == expected
    
    def test_to_sheets_value_plain_type_with_validation(self):
        """Test conversion to Sheets format for PLAIN type with validation."""
        validation = {"condition": {"type": "ONE_OF_LIST"}}
        cell = CellData("test", CellType.PLAIN, validation=validation)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "test"},
            "dataValidation": validation
        }
        assert result == expected
    
    def test_to_sheets_value_plain_type_with_protection(self):
        """Test conversion to Sheets format for PLAIN type with protection."""
        cell = CellData("test", CellType.PLAIN, protection=True)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "test"},
            "userEnteredFormat": {}
        }
        assert result == expected
    
    def test_to_sheets_value_formula_type(self):
        """Test conversion to Sheets format for FORMULA type."""
        cell = CellData("=SUM(A1:A10)", CellType.FORMULA)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"formulaValue": "=SUM(A1:A10)"}
        }
        assert result == expected
    
    def test_to_sheets_value_formula_type_with_formatting(self):
        """Test conversion to Sheets format for FORMULA type with formatting."""
        formatting = {"numberFormat": {"type": "CURRENCY"}}
        cell = CellData("=A1*B1", CellType.FORMULA, formatting=formatting)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"formulaValue": "=A1*B1"},
            "userEnteredFormat": formatting
        }
        assert result == expected
    
    def test_to_sheets_value_rich_text_type_basic(self):
        """Test conversion to Sheets format for RICH_TEXT type without format runs."""
        rich_text_value = {"text": "Hello World"}
        cell = CellData(rich_text_value, CellType.RICH_TEXT)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "Hello World"}
        }
        assert result == expected
    
    def test_to_sheets_value_rich_text_type_with_format_runs(self):
        """Test conversion to Sheets format for RICH_TEXT type with format runs."""
        rich_text_value = {
            "text": "Hello World",
            "format_runs": [
                {
                    "startIndex": 0,
                    "format": {
                        "link": {"uri": "https://example.com"},
                        "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 1.0},
                        "underline": True
                    }
                }
            ]
        }
        cell = CellData(rich_text_value, CellType.RICH_TEXT)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "Hello World"},
            "textFormatRuns": [
                {
                    "startIndex": 0,
                    "format": {
                        "link": {"uri": "https://example.com"},
                        "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 1.0},
                        "underline": True
                    }
                }
            ]
        }
        assert result == expected
    
    def test_to_sheets_value_rich_text_empty_text(self):
        """Test conversion to Sheets format for RICH_TEXT type with empty text."""
        rich_text_value = {"text": ""}
        cell = CellData(rich_text_value, CellType.RICH_TEXT)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": ""}
        }
        assert result == expected
    
    def test_to_sheets_value_empty_cell_none(self):
        """Test conversion to Sheets format for empty cell (None value)."""
        cell = CellData(None, CellType.PLAIN)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": None
        }
        assert result == expected
    
    def test_to_sheets_value_empty_cell_empty_string(self):
        """Test conversion to Sheets format for empty cell (empty string)."""
        cell = CellData("", CellType.PLAIN)  # This becomes None in __init__
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": None
        }
        assert result == expected
    
    def test_to_sheets_value_empty_cell_whitespace(self):
        """Test conversion to Sheets format for empty cell (whitespace)."""
        cell = CellData("   ", CellType.PLAIN)  # This becomes None in __init__
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": None
        }
        assert result == expected
    
    def test_to_sheets_value_non_string_value(self):
        """Test conversion to Sheets format for non-string values."""
        cell = CellData(42, CellType.PLAIN)
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "42"}
        }
        assert result == expected
    
    def test_to_sheets_value_combined_options(self):
        """Test conversion to Sheets format with multiple options."""
        formatting = {"textFormat": {"bold": True}}
        validation = {"condition": {"type": "ONE_OF_LIST"}}
        
        cell = CellData(
            "test",
            CellType.PLAIN,
            formatting=formatting,
            validation=validation,
            protection=True
        )
        result = cell.to_sheets_value()
        
        expected = {
            "userEnteredValue": {"stringValue": "test"},
            "userEnteredFormat": formatting,
            "dataValidation": validation
        }
        assert result == expected
    
    def test_to_sheets_value_protection_without_formatting(self):
        """Test that protection adds userEnteredFormat when not present."""
        cell = CellData("test", CellType.PLAIN, protection=True)
        result = cell.to_sheets_value()
        
        assert "userEnteredFormat" in result
        assert result["userEnteredFormat"] == {}
    
    def test_to_sheets_value_protection_with_existing_formatting(self):
        """Test that protection doesn't override existing formatting."""
        formatting = {"textFormat": {"bold": True}}
        cell = CellData("test", CellType.PLAIN, formatting=formatting, protection=True)
        result = cell.to_sheets_value()
        
        assert result["userEnteredFormat"] == formatting
    
    def test_rich_text_format_runs_partial_format(self):
        """Test rich text with format runs that have partial format data."""
        rich_text_value = {
            "text": "Test",
            "format_runs": [
                {
                    "startIndex": 0,
                    "format": {
                        "link": {"uri": "https://example.com"}
                        # Missing foregroundColor and underline
                    }
                }
            ]
        }
        cell = CellData(rich_text_value, CellType.RICH_TEXT)
        result = cell.to_sheets_value()
        
        expected_format_runs = [
            {
                "startIndex": 0,
                "format": {
                    "link": {"uri": "https://example.com"},
                    "foregroundColor": None,
                    "underline": None
                }
            }
        ]
        
        assert result["textFormatRuns"] == expected_format_runs
    
    def test_rich_text_multiple_format_runs(self):
        """Test rich text with multiple format runs."""
        rich_text_value = {
            "text": "Hello World",
            "format_runs": [
                {
                    "startIndex": 0,
                    "format": {
                        "link": {"uri": "https://example.com"},
                        "foregroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0},
                        "underline": True
                    }
                },
                {
                    "startIndex": 6,
                    "format": {
                        "link": {"uri": "https://another.com"},
                        "foregroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0},
                        "underline": False
                    }
                }
            ]
        }
        cell = CellData(rich_text_value, CellType.RICH_TEXT)
        result = cell.to_sheets_value()
        
        assert len(result["textFormatRuns"]) == 2
        assert result["textFormatRuns"][0]["startIndex"] == 0
        assert result["textFormatRuns"][1]["startIndex"] == 6
