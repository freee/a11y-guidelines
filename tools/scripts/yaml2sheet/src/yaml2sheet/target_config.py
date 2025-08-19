"""Target and platform configuration constants for yaml2sheet."""

from .types import M17nField
from typing import Dict, List

# Language support
LANGS: List[str] = ['ja', 'en']

# Sheet configuration constants
HEADER_ROW: int = 1
CHECKLIST_VERSION_CELL: str = 'A27'
SHEET_INDEX_TARGET_ROW: int = 7

# Target platform names
TARGET_NAMES: Dict[str, M17nField] = {
    'designWeb': {'ja': 'デザイン: Web', 'en': 'Design: Web'},
    'designMobile': {'ja': 'デザイン: モバイルアプリ', 'en': 'Design: Mobile App'},
    'codeWeb': {'ja': 'コード: Web', 'en': 'Code: Web'},
    'codeMobile': {'ja': 'コード: モバイルアプリ', 'en': 'Code: Mobile App'},
    'productWeb': {'ja': 'プロダクト: Web', 'en': 'Product: Web'},
    'productIos': {'ja': 'プロダクト: iOSアプリ', 'en': 'Product: iOS App'},
    'productAndroid': {'ja': 'プロダクト: Androidアプリ', 'en': 'Product: Android App'}
}
