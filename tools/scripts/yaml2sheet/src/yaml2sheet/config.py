from typing import TypedDict, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum

# Type definitions
class M17nField(TypedDict):
    ja: str
    en: str

class Link(TypedDict):
    text: M17nField
    url: M17nField

class ConditionStatement(TypedDict):
    platform: str
    summary: M17nField

class Procedure(TypedDict):
    id: str
    platform: str
    target: str
    tool: str
    procedure: M17nField
    toolLink: Link

class Condition(TypedDict):
    type: str
    platform: str
    target: str
    procedure: Procedure
    conditions: List['Condition']
    conditionStatements: List[ConditionStatement]

class Check(TypedDict):
    id: str
    checkId: str
    subcheckId: str
    sortKey: Union[int, None]
    target: str
    platform: List[str]
    severity: str
    check: M17nField
    result: Union[M17nField, None]
    conditions: Union[List[Condition], None]
    guidelines: Union[List[Link], None]
    info: Union[List[Link], None]
    isSubcheck: Union[bool, None]
    subchecks: Union[Dict[str, Dict[str, Union[int, List[Any]]]], None]

class ColumnSetByTarget(TypedDict):
    plainData1: List[str]
    plainData2: List[str]
    linkData: List[str]
    generatedData: List[str]

class ColumnSet(TypedDict):
    idCols: List[str]
    userEntered: List[str]
    common: ColumnSetByTarget
    designWeb: ColumnSetByTarget
    designMobile: ColumnSetByTarget
    codeWeb: ColumnSetByTarget
    codeMobile: ColumnSetByTarget
    productWeb: ColumnSetByTarget
    productIos: ColumnSetByTarget
    productAndroid: ColumnSetByTarget

class ColumnInfo(TypedDict):
    name: Dict[str, M17nField]
    width: Dict[str, int]

# Constants
LANGS = ['ja', 'en']
HEADER_ROW = 1
CHECKLIST_VERSION_CELL = 'A27'
SHEET_INDEX_TARGET_ROW = 7

TARGET_NAMES = {
    'designWeb': {'ja': 'デザイン: Web', 'en': 'Design: Web'},
    'designMobile': {'ja': 'デザイン: モバイルアプリ', 'en': 'Design: Mobile App'},
    'codeWeb': {'ja': 'コード: Web', 'en': 'Code: Web'},
    'codeMobile': {'ja': 'コード: モバイルアプリ', 'en': 'Code: Mobile App'},
    'productWeb': {'ja': 'プロダクト: Web', 'en': 'Product: Web'},
    'productIos': {'ja': 'プロダクト: iOSアプリ', 'en': 'Product: iOS App'},
    'productAndroid': {'ja': 'プロダクト: Androidアプリ', 'en': 'Product: Android App'}
}

CHECK_RESULTS = {
    'unchecked': {'ja': '未チェック', 'en': 'UNCHECKED'},
    'pass': {'ja': 'はい', 'en': 'TRUE'},
    'fail': {'ja': 'いいえ', 'en': 'FALSE'}
}

FINAL_CHECK_RESULTS = {
    'unchecked': {'ja': '未チェック', 'en': 'UNCHECKED'},
    'pass': {'ja': 'OK', 'en': 'PASS'},
    'fail': {'ja': 'NG', 'en': 'FAIL'}
}

COLUMNS = {
    "idCols": ["checkId", "subcheckId"],
    "userEntered": ["result", "note"],
    "common": {
        "plainData1": ["check"],
        "plainData2": ["severity"],
        "linkData": ["info", "guidelines"],
        "generatedData": []
    },
    "designWeb": {
        "plainData1": ["webConditionStatement"],
        "plainData2": [],
        "linkData": [],
        "generatedData": ["finalResult", "calculatedResult"]
    },
    "designMobile": {
        "plainData1": [],
        "plainData2": [],
        "linkData": [],
        "generatedData": []
    },
    "codeWeb": {
        "plainData1": ["implementation_web"],
        "plainData2": [],
        "linkData": [],
        "generatedData": []
    },
    "codeMobile": {
        "plainData1": ["implementation_ios", "implementation_android"],
        "plainData2": [],
        "linkData": [],
        "generatedData": []
    },
    "productWeb": {
        "plainData1": ["webConditionStatement"],
        "plainData2": [],
        "linkData": ["webTools"],
        "generatedData": ["finalResult", "calculatedResult"]
    },
    "productIos": {
        "plainData1": ["iosConditionStatement"],
        "plainData2": [],
        "linkData": ["iosTools"],
        "generatedData": ["finalResult", "calculatedResult"]
    },
    "productAndroid": {
        "plainData1": ["androidConditionStatement"],
        "plainData2": [],
        "linkData": ["androidTools"],
        "generatedData": ["finalResult", "calculatedResult"]
    }
}

COLUMN_INFO = {
    "name": {
        "checkId": {"ja": "ID", "en": "ID"},
        "subcheckId": {"ja": "ID", "en": "ID"},
        "finalResult": {"ja": "最終結果", "en": "Final Result"},
        "calculatedResult": {"ja": "判定結果（自動）", "en": "Final Result (Auto)"},
        "result": {"ja": "チェック結果を記入", "en": "Fill in the Check Result"},
        "note": {"ja": "チェック結果に関する補足", "en": "Note on Check Result"},
        "check": {"ja": "チェック内容", "en": "Check Details"},
        "severity": {"ja": "重篤度", "en": "Severity"},
        "implementation_web": {"ja": "実装方法：Web", "en": "Implementation: Web"},
        "implementation_ios": {"ja": "実装方法：iOS", "en": "Implementation: iOS"},
        "implementation_android": {"ja": "実装方法：Android", "en": "Implementation: Android"},
        "webConditionStatement": {"ja": "チェック手順", "en": "Check Procedure"},
        "iosConditionStatement": {"ja": "チェック手順", "en": "Check Procedure"},
        "androidConditionStatement": {"ja": "チェック手順", "en": "Check Procedure"},
        "webTools": {"ja": "チェック・ツール", "en": "Check Tools"},
        "iosTools": {"ja": "チェック・ツール", "en": "Check Tools"},
        "androidTools": {"ja": "チェック・ツール", "en": "Check Tools"},
        "info": {"ja": "参考情報", "en": "Supplemental Info"},
        "guidelines": {"ja": "関連ガイドライン", "en": "Related Guidelines"}
    },
    "width": {
        "checkId": 43,
        "subcheckId": 170,
        "finalResult": 208,
        "calculatedResult": 140,
        "result": 140,
        "note": 306,
        "check": 312,
        "severity": 158,
        "implementation_web": 312,
        "implementation_ios": 312,
        "implementation_android": 312,
        "webConditionStatement": 312,
        "iosConditionStatement": 312,
        "androidConditionStatement": 312,
        "webTools": 77,
        "iosTools": 140,
        "androidTools": 140,
        "info": 313,
        "guidelines": 628,
    }
}
