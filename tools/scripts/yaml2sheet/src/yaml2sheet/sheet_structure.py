from typing import List, Dict, Optional
from dataclasses import dataclass, field
from .cell_data import CellData


@dataclass
class ColumnProperties:
    """Properties for a spreadsheet column"""
    width: int
    hidden: bool = False


@dataclass
class SheetStructure:
    """Complete structure of a spreadsheet sheet"""
    name: str
    sheet_id: Optional[int]
    columns: List[ColumnProperties] = field(default_factory=list)
    frozen_rows: int = 1
    frozen_columns: int = 0
    data: List[List[CellData]] = field(default_factory=list)
    conditional_formats: List[Dict] = field(default_factory=list)
    protected_ranges: List[Dict] = field(default_factory=list)


@dataclass
class CheckInfo:
    """Information about a check item"""
    id: str
    is_subcheck: bool
    subchecks_by_target: Dict[str, int]  # Target to subcheck count mapping
