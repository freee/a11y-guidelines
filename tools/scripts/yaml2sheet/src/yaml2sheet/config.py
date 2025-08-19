"""Configuration module for yaml2sheet - provides backward compatibility imports."""

# Import type definitions
from .types import (
    M17nField, Link, ConditionStatement, Procedure, Condition, Check,
    ColumnSetByTarget, ColumnSet, ColumnInfo
)

# Import configuration constants from specialized modules
from .target_config import LANGS, HEADER_ROW, CHECKLIST_VERSION_CELL, SHEET_INDEX_TARGET_ROW, TARGET_NAMES
from .result_config import CHECK_RESULTS, FINAL_CHECK_RESULTS
from .column_config import COLUMNS, COLUMN_INFO

# Re-export all constants for backward compatibility
__all__ = [
    # Types
    'M17nField', 'Link', 'ConditionStatement', 'Procedure', 'Condition', 'Check',
    'ColumnSetByTarget', 'ColumnSet', 'ColumnInfo',
    # Constants
    'LANGS', 'HEADER_ROW', 'CHECKLIST_VERSION_CELL', 'SHEET_INDEX_TARGET_ROW',
    'TARGET_NAMES', 'CHECK_RESULTS', 'FINAL_CHECK_RESULTS', 'COLUMNS', 'COLUMN_INFO'
]
