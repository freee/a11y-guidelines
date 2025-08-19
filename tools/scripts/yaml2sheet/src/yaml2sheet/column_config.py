"""Column configuration constants for yaml2sheet."""

from .types import ColumnSet, ColumnInfo

# Column structure definition
COLUMNS: ColumnSet = {
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

# Column information (names and widths)
COLUMN_INFO: ColumnInfo = {
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
        "implementation_android": {
            "ja": "実装方法：Android", "en": "Implementation: Android"
        },
        "webConditionStatement": {"ja": "チェック手順", "en": "Check Procedure"},
        "iosConditionStatement": {
            "ja": "チェック手順", "en": "Check Procedure"
        },
        "androidConditionStatement": {
            "ja": "チェック手順", "en": "Check Procedure"
        },
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
