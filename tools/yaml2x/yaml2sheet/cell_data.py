from typing import Any, Dict, Optional
from enum import Enum

class CellType(Enum):
    """Cell data type enumeration"""
    PLAIN = "plain"
    RICH_TEXT = "rich_text"
    FORMULA = "formula"

class CellData:
    """Represents a cell's data structure and formatting"""
    
    def __init__(
        self,
        value: Any,
        type: CellType,
        formatting: Optional[Dict] = None,
        validation: Optional[Dict] = None,
        protection: bool = False,
        note: Optional[str] = None
    ):
        """Initialize cell data with value and formatting options
        
        Args:
            value: Cell value (string, number, formula, or rich text object)
            type: CellType enum indicating data type
            formatting: Optional dictionary of cell formatting options
            validation: Optional dictionary of data validation rules
            protection: Whether the cell is protected
            note: Optional cell comment/note
        """
        self.value = value
        self.type = type
        self.formatting = formatting
        self.validation = validation
        self.protection = protection
        self.note = note
    
    def to_sheets_value(self) -> Dict:
        """Convert cell data to Google Sheets API format
        
        Returns:
            Dict: Cell data in Google Sheets API format
        """
        result = {}
        
        # Set cell value based on type
        if self.type == CellType.PLAIN:
            result["userEnteredValue"] = {"stringValue": str(self.value)}
        elif self.type == CellType.RICH_TEXT:
            result["userEnteredValue"] = {"stringValue": self.value['text']}
            # Process text format runs if present
            if self.value['format_runs']:
                result["textFormatRuns"] = [
                    {
                        "startIndex": run['startIndex'],
                        "format": {
                            "link": run['format'].get('link'),
                            "foregroundColor": run['format'].get('foregroundColor'),
                            "underline": run['format'].get('underline')
                        }
                    }
                    for run in self.value['format_runs']
                ]
        elif self.type == CellType.FORMULA:
            result["userEnteredValue"] = {"formulaValue": self.value}

        # Add formatting if specified
        if self.formatting:
            result["userEnteredFormat"] = self.formatting

        # Add data validation rules if specified
        if self.validation:
            result["dataValidation"] = self.validation

        return result
