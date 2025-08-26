"""Result configuration constants for yaml2sheet."""

from .types import M17nField
from typing import Dict

# Check result definitions
CHECK_RESULTS: Dict[str, M17nField] = {
    'unchecked': {'ja': '未チェック', 'en': 'UNCHECKED'},
    'pass': {'ja': 'はい', 'en': 'TRUE'},
    'fail': {'ja': 'いいえ', 'en': 'FALSE'}
}

FINAL_CHECK_RESULTS: Dict[str, M17nField] = {
    'unchecked': {'ja': '未チェック', 'en': 'UNCHECKED'},
    'pass': {'ja': 'OK', 'en': 'PASS'},
    'fail': {'ja': 'NG', 'en': 'FAIL'}
}
