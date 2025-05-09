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
        # 空文字列の場合は None に変換して完全に空のセルとして扱う
        if isinstance(value, str) and not value.strip() and type == CellType.PLAIN:
            self.value = None
        else:
            self.value = value
            
        self.type = type
        
        # 値が None の場合は書式設定も適用しない（完全に空のセルにする）
        if self.value is None:
            self.formatting = None
        else:
            self.formatting = formatting
            
        self.validation = validation
        self.protection = protection
        self.note = note

    def to_sheets_value(self) -> Dict:
        """Convert cell data to Google Sheets API format, ensuring empty cells are truly empty
        
        Returns:
            Dict: Cell data in Google Sheets API format
        """
        result = {}
        
        is_empty = self.value is None or (isinstance(self.value, str) and not self.value.strip())
        
        if is_empty:
            result["userEnteredValue"] = None
        else:
            if self.type == CellType.PLAIN:
                result["userEnteredValue"] = {"stringValue": str(self.value) if self.value is not None else ""}
            elif self.type == CellType.RICH_TEXT:
                result["userEnteredValue"] = {"stringValue": self.value.get('text', '')}
                if self.value.get('format_runs'):
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
                
            if self.formatting:
                result["userEnteredFormat"] = self.formatting

        if self.validation:
            result["dataValidation"] = self.validation
            
        if self.protection and "userEnteredFormat" not in result:
            result["userEnteredFormat"] = {}

        return result
