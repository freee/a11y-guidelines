from typing import Dict, List, Any, Optional, TypedDict, Union, Tuple
from dataclasses import dataclass, field
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
from datetime import datetime
import pytz
from enum import Enum
import os.path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Config
SPREADSHEET_ID = os.getenv('CHECKSHEET_ID')
SOURCE_FILE = 'checks-v5.json'

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
    sortKey: Optional[int]
    target: str
    platform: List[str]
    severity: str
    check: M17nField
    result: Optional[M17nField]
    conditions: Optional[List[Condition]]
    guidelines: Optional[List[Link]]
    info: Optional[List[Link]]
    isSubcheck: Optional[bool]
    subchecks: Optional[Dict[str, Dict[str, Union[int, List[Any]]]]]

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
        "plainData1": [],
        "plainData2": [],
        "linkData": [],
        "generatedData": []
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
        "checkId": {
            "ja": "ID",
            "en": "ID"
        },
        "subcheckId": {
            "ja": "ID",
            "en": "ID"
        },
        "finalResult": {
            "ja": "最終結果",
            "en": "Final Result"
        },
        "calculatedResult": {
            "ja": "判定結果（自動）",
            "en": "Final Result (Auto)"
        },
        "result": {
            "ja": "チェック結果を記入",
            "en": "Fill in the Check Result"
        },
        "note": {
            "ja": "チェック結果に関する補足",
            "en": "Note on Check Result"
        },
        "check": {
            "ja": "チェック内容",
            "en": "Check Details"
        },
        "severity": {
            "ja": "重篤度",
            "en": "Severity"
        },
        "implementation_web": {
            "ja": "実装方法：Web",
            "en": "Implementation: Web"
        },
        "implementation_ios": {
            "ja": "実装方法：iOS",
            "en": "Implementation: iOS"
        },
        "implementation_android": {
            "ja": "実装方法：Android",
            "en": "Implementation: Android"
        },
        "webConditionStatement": {
            "ja": "チェック手順",
            "en": "Check Procedure"
        },
        "iosConditionStatement": {
            "ja": "チェック手順",
            "en": "Check Procedure"
        },
        "androidConditionStatement": {
            "ja": "チェック手順",
            "en": "Check Procedure"
        },
        "webTools": {
            "ja": "チェック・ツール",
            "en": "Check Tools"
        },
        "iosTools": {
            "ja": "チェック・ツール",
            "en": "Check Tools"
        },
        "androidTools": {
            "ja": "チェック・ツール",
            "en": "Check Tools"
        },
        "info": {
            "ja": "参考情報",
            "en": "Supplemental Info"
        },
        "guidelines": {
            "ja": "関連ガイドライン",
            "en": "Related Guidelines"
        }
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

# Cell data structure
class CellType(Enum):
    PLAIN = "plain"
    RICH_TEXT = "rich_text"
    FORMULA = "formula"

@dataclass
class CellData:
    value: Any
    type: CellType
    formatting: Optional[Dict] = None
    validation: Optional[Dict] = None
    protection: bool = False
    note: Optional[str] = None
    
    def to_sheets_value(self) -> Dict:
        """セルのデータをSheetsのAPI形式に変換"""
        result = {}
        
        # 値の設定
        if self.type == CellType.PLAIN:
            result["userEnteredValue"] = {"stringValue": str(self.value)}
        elif self.type == CellType.RICH_TEXT:
            result["userEnteredValue"] = {"stringValue": self.value['text']}
            # テキストフォーマットランの処理
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

        # 書式設定
        if self.formatting:
            result["userEnteredFormat"] = self.formatting

        # データ検証ルール
        if self.validation:
            result["dataValidation"] = self.validation

        return result

@dataclass
class ColumnProperties:
    width: int
    hidden: bool = False

@dataclass
class SheetStructure:
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
    """チェック項目の情報を保持するクラス"""
    id: str
    is_subcheck: bool
    subchecks_by_target: Dict[str, int]  # ターゲットごとのサブチェック数

class ChecklistSheetGenerator:
    def __init__(self, credentials: Credentials, spreadsheet_id: str):
        self.service = build('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id
        self.sheets: Dict[str, SheetStructure] = {}
        self.existing_sheets: Dict[str, Dict[str, Any]] = {}
        self.current_lang: str = 'ja'  # 現在の言語
        self.current_target: str = ''   # 現在のターゲット
        self.current_parent_formula: Optional[str] = None  # 追加
        self._load_existing_sheets()
        self.check_info: Dict[str, CheckInfo] = {}  # チェック情報を保持

    def _load_existing_sheets(self):
        """スプレッドシートの既存シート情報を取得"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            logger.debug("Loading existing sheets")            
            for sheet in spreadsheet.get('sheets', []):
                properties = sheet['properties']
                title = properties['title']
                logger.debug(f"Found existing sheet: '{title}'")
                self.existing_sheets[properties['title']] = {
                    'sheetId': properties['sheetId'],
                    'index': properties.get('index', 0)
                }
            logger.debug(f"Loaded existing sheets: {list(self.existing_sheets.keys())}")
        except Exception as e:
            logger.error(f"Error loading existing sheets: {e}")
            raise

    def _clear_sheet_content(self, sheet_id: int) -> Dict:
        """シートの内容をクリアするリクエストを生成"""
        return {
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'startColumnIndex': 0
                },
                'fields': '*'
            }
        }

    def initialize_spreadsheet(self) -> None:
        """スプレッドシートの初期化（2枚目以降のシートを削除）"""
        try:
            # スプレッドシートの情報を取得
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            # 2枚目以降のシートがあれば削除
            if len(spreadsheet.get('sheets', [])) > 1:
                delete_requests = []
                for sheet in spreadsheet['sheets'][1:]:  # 最初のシート以外
                    delete_requests.append({
                        'deleteSheet': {
                            'sheetId': sheet['properties']['sheetId']
                        }
                    })
                
                if delete_requests:
                    self.service.spreadsheets().batchUpdate(
                        spreadsheetId=self.spreadsheet_id,
                        body={'requests': delete_requests}
                    ).execute()
                    logger.info("Deleted existing sheets except the first one")
            
            # 既存シート情報をクリア
            self.existing_sheets = {
                spreadsheet['sheets'][0]['properties']['title']: {
                    'sheetId': spreadsheet['sheets'][0]['properties']['sheetId'],
                    'index': 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error initializing spreadsheet: {e}")
            raise

    def prepare_sheet_structure(self, target_id: str, target_name: str, lang: str, checks: List[Check]) -> SheetStructure:
        """シート構造を準備"""
        # 現在の言語とターゲットを設定
        self.current_lang = lang
        self.current_target = target_id
        
        logger.info(f"Preparing sheet structure: target_id={target_id}, target_name={target_name}, lang={lang}")
        sheet = SheetStructure(name=target_name, sheet_id=None)

        # ヘッダーの準備
        headers = self.get_headers(target_id, lang)  # Note: get_headersはtarget_idを使用
        header_row = []
        for header in headers:
            header_row.append(CellData(
                value=header,
                type=CellType.PLAIN,
                formatting={"textFormat": {"bold": True}}
            ))
        sheet.data.append(header_row)
        
        # ID to Row のマッピング生成の準備
        id_to_row = {}
        current_row = 2  # ヘッダー行の次から
        
        # 最初にすべてのチェックとサブチェックの行番号を計算
        for check in checks:
            if check.get('isSubcheck'):
                # サブチェックの場合は飛ばす（親チェックの処理時に登録される）
                continue
                
            logger.debug(f"Processing check {check['id']} at row {current_row}")
            # メインチェックのIDを登録
            id_to_row[check['id']] = current_row
            
            # メインチェックの手順IDを登録（条件がある場合）
            if check.get('conditions'):
                for condition in check['conditions']:
                    if condition['target'] == target_id:
                        if condition['type'] == 'simple':
                            proc_id = condition['procedure']['id']
                            id_to_row[proc_id] = current_row
                            logger.debug(f"Registering procedure {proc_id} at row {current_row}")
                        else:
                            self.collect_procedure_ids(condition, id_to_row, current_row)

            # サブチェックの処理
            subchecks = check.get('subchecks', {}).get(target_id, {})
            if subchecks and 'conditions' in subchecks:
                subcheck_count = len(subchecks['conditions'])
                logger.debug(f"Found {subcheck_count} subchecks for check {check['id']}")
                
                # サブチェックの行番号を登録
                for i, subcheck in enumerate(subchecks['conditions'], start=1):
                    subcheck_row = current_row + i
                    subcheck_id = subcheck['id']
                    id_to_row[subcheck_id] = subcheck_row
                    logger.debug(f"Registering subcheck {subcheck_id} at row {subcheck_row}")
                    
                    # サブチェックの手順IDも登録
                    if subcheck.get('conditions'):
                        for condition in subcheck['conditions']:
                            if condition['type'] == 'simple':
                                proc_id = condition['procedure']['id']
                                id_to_row[proc_id] = subcheck_row
                                logger.debug(f"Registering subcheck procedure {proc_id} at row {subcheck_row}")
                            else:
                                self.collect_procedure_ids(condition, id_to_row, subcheck_row)
                
                current_row += subcheck_count
                
            current_row += 1

        logger.debug(f"Final id_to_row mapping: {id_to_row}")

        # データ行の準備
        for check in checks:
            row_data = self.prepare_row_data(check, target_id, lang, id_to_row)
            sheet.data.append(row_data)
        
        # 条件付き書式の準備
        data_length = len(sheet.data)
        sheet.conditional_formats.extend(self.get_conditional_formats(target_id, data_length, lang))
        
        return sheet

    def collect_procedure_ids(self, condition: Condition, id_to_row: Dict[str, int], row: int) -> None:
        """条件から手順IDを収集して登録する"""
        if condition['type'] == 'simple':
            id_to_row[condition['procedure']['id']] = row
        else:
            for cond in condition['conditions']:
                self.collect_procedure_ids(cond, id_to_row, row)

    def prepare_rich_text_cell(self, links: List[Link], lang: str) -> CellData:
        """リッチテキストセルの準備"""
        text_parts = []
        format_runs = []
        current_index = 0
        
        for i, link in enumerate(links):
            if i > 0:  # 最初のリンク以外の前に改行を追加
                text_parts.append("\n")
                current_index += 1
                
            link_text = link['text'][lang]
            text_parts.append(link_text)
            
            format_runs.append({
                'startIndex': current_index,
                'format': {
                    'link': {'uri': link['url'][lang]},
                    'foregroundColor': {'red': 0.06, 'green': 0.47, 'blue': 0.82},
                    'underline': True
                }
            })
            current_index += len(link_text)
        
        value = {
            'text': ''.join(text_parts),
            'format_runs': format_runs
        }
            
        return CellData(
            value=value,
            type=CellType.RICH_TEXT
        )

    def get_conditional_formats(self, target_id: str, data_length: int, lang: str) -> List[Dict]:
        """条件付き書式の設定を生成する"""
        has_generated_data = bool(COLUMNS[target_id]['generatedData'])
        if not has_generated_data:
            return []

        result_column = self.get_result_column_index()
        
        formats = []
        # PASS（OKまたはTRUE）の場合の書式
        formats.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'startRowIndex': 1,  # ヘッダー行の次から
                        'endRowIndex': data_length,
                        'startColumnIndex': result_column - 1,  # CalculatedResult列（D列）
                        'endColumnIndex': result_column + 1    # 結果列（E列）まで
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['pass'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}  # 薄い緑
                        }
                    }
                }
            }
        })
        
        # PASS（PASS）の場合の書式
        formats.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'startRowIndex': 1,  # ヘッダー行の次から
                        'endRowIndex': data_length,
                        'startColumnIndex': result_column - 1,  # CalculatedResult列（D列）
                        'endColumnIndex': result_column + 1    # 結果列（E列）まで
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': FINAL_CHECK_RESULTS['pass'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}  # 薄い緑
                        }
                    }
                }
            }
        })

        # FAIL（NGまたはFALSE）の場合の書式
        formats.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'startRowIndex': 1,  # ヘッダー行の次から
                        'endRowIndex': data_length,
                        'startColumnIndex': result_column - 1,  # CalculatedResult列（D列）
                        'endColumnIndex': result_column + 1    # 結果列（E列）まで
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['fail'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.96, 'green': 0.80, 'blue': 0.80}  # 薄い赤
                        }
                    }
                }
            }
        })

        # FAIL（FAIL）の場合の書式
        formats.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'startRowIndex': 1,  # ヘッダー行の次から
                        'endRowIndex': data_length,
                        'startColumnIndex': result_column - 1,  # CalculatedResult列（D列）
                        'endColumnIndex': result_column + 1    # 結果列（E列）まで
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': FINAL_CHECK_RESULTS['fail'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.96, 'green': 0.80, 'blue': 0.80}  # 薄い赤
                        }
                    }
                }
            }
        })

        return formats

    def update_conditional_formats(self, formats: List[Dict], sheet_id: int) -> List[Dict]:
        """条件付き書式のsheet_idを更新する
        
        Args:
            formats: 条件付き書式のリクエストリスト
            sheet_id: 新しいシートID
            
        Returns:
            List[Dict]: 更新された条件付き書式のリクエスト
        """
        updated_formats = []
        for format_rule in formats:
            if 'addConditionalFormatRule' in format_rule:
                # deep copyで新しいオブジェクトを作成
                new_rule = json.loads(json.dumps(format_rule))
                ranges = new_rule['addConditionalFormatRule']['rule']['ranges']
                # 各rangeにsheet_idを設定
                for range_obj in ranges:
                    range_obj['sheetId'] = sheet_id
                updated_formats.append(new_rule)
        return updated_formats

    def generate_batch_requests(self) -> tuple[List[Dict], Dict]:
        """バッチ更新リクエストを生成"""
        requests = []
        pending_formats = {}

        logger.info(f"Generating requests for sheets: {list(self.sheets.keys())}")

        for sheet_name, sheet in self.sheets.items():
            data_length = len(sheet.data)
            column_count = len(sheet.data[0]) if sheet.data else 26

            logger.debug(f"Processing sheet '{sheet_name}', exists: {sheet_name in self.existing_sheets}")
            logger.debug(f"Existing sheets: {list(self.existing_sheets.keys())}")

            # ターゲットIDを特定（言語を考慮）
            target_id = None
            current_lang = None
            for tid, translations in TARGET_NAMES.items():
                for lang, name in translations.items():
                    if name == sheet_name:
                        target_id = tid
                        current_lang = lang
                        self.current_lang = lang
                        self.current_target = tid
                        break
                if target_id:
                    break

            logger.debug(f"Found target_id: {target_id}, lang: {current_lang} for sheet: {sheet_name}")
            
            if target_id is None:
                logger.warning(f"Could not find target_id for sheet: {sheet_name}")
                continue

            sheet_exists = sheet_name in self.existing_sheets
            
            if sheet_exists:
                # 既存シートの処理
                sheet_id = self.existing_sheets[sheet_name]['sheetId']
                logger.debug(f"Updating existing sheet: {sheet_name} (id: {sheet_id})")
                requests.append(self._clear_sheet_content(sheet_id))
                requests.extend(self.prepare_sheet_content(sheet_id, sheet))
                requests.extend(self.apply_basic_formatting(sheet_id, data_length))
                # requests.extend(self.add_basic_data_validation(sheet_id, data_length, target_id, current_lang))
                requests.extend(self.add_conditional_formatting(sheet_id, data_length, current_lang))
            else:
                # 新規シート作成
                logger.info(f"Creating new sheet: {sheet_name} with {column_count} columns")
                create_request = {
                    'addSheet': {
                        'properties': {
                            'title': sheet_name,
                            'gridProperties': {
                                'rowCount': max(data_length + 1, 1000),
                                'columnCount': column_count
                            }
                        }
                    }
                }
                requests.append(create_request)
                
                pending_formats[sheet_name] = {
                    'data_length': data_length,
                    'formats': []
                }

        logger.info(f"Total requests generated: {len(requests)}")
        logger.info(f"Sheet creation requests: {[req.get('addSheet', {}).get('properties', {}).get('title') for req in requests if 'addSheet' in req]}")

        return requests, pending_formats

    def execute_batch_update(self):
        """バッチ更新を実行"""
        try:
            # 最初のバッチ更新（シートの作成など）
            initial_requests, pending_formats = self.generate_batch_requests()
            
            # シート作成のリクエストのみを実行
            creation_requests = [req for req in initial_requests if 'addSheet' in req]
            if creation_requests:
                logger.info(f"Creating sheets: {[req.get('addSheet', {}).get('properties', {}).get('title') for req in creation_requests]}")
                creation_response = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': creation_requests}
                ).execute()
                
                # 新規シートのIDを取得してexisting_sheetsを更新
                for reply in creation_response.get('replies', []):
                    if 'addSheet' in reply:
                        sheet_id = reply['addSheet']['properties']['sheetId']
                        sheet_title = reply['addSheet']['properties']['title']
                        self.existing_sheets[sheet_title] = {
                            'sheetId': sheet_id,
                            'index': 0  # 仮の値
                        }

            # 残りの更新リクエストを生成（新規シート含む全シート対象）
            update_requests, _ = self.generate_batch_requests()
            update_requests = [req for req in update_requests if 'addSheet' not in req]
            
            # バージョン情報の更新リクエストを追加
            update_requests = [req for req in initial_requests if 'addSheet' not in req]
            if hasattr(self, 'version_update_request'):  # バージョン情報更新リクエストが存在する場合
                update_requests.append(self.version_update_request)

            if update_requests:
                logger.info(f"Updating {len(update_requests)} sheet contents")
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': update_requests}
                ).execute()
                            
        except Exception as e:
            logger.error(f"Error executing batch update: {e}")
            raise

    def process_source_data(self, src: Dict[str, Any]) -> Dict[str, List[Check]]:
        """ソースデータを処理してシート生成用のデータに変換する
        
        Args:
            src: JSONから読み込んだチェックリストのソースデータ
            
        Returns:
            Dict[str, List[Check]]: ターゲット識別子をキーとし、チェック項目のリストを値とする辞書
        """

        # ターゲットごとのチェックリストを初期化
        # ここではM17nFieldを持つシート名ではなく、ターゲット識別子をキーとして使用
        processed_data = {target: [] for target in TARGET_NAMES.keys()}
        
        # チェック項目をsortKeyでソート
        sorted_entries = sorted(src.items(), key=lambda x: x[1].get('sortKey', 0))
        
        for key, check in sorted_entries:
            # 基本フィールドの設定
            check['checkId'] = check['id']
            check['subcheckId'] = ""
            
            # モバイルプラットフォームの展開
            if 'mobile' in check['platform']:
                check['platform'].extend(['ios', 'android'])

            # シート名（ターゲット識別子）の設定
            check['sheetNames'] = []
            for platform in check['platform']:
                target_id = f"{check['target']}{platform.capitalize()}"
                if target_id not in TARGET_NAMES:
                    continue
                check['sheetNames'].append(target_id)
                
            # 生成データが必要なシートの場合の処理
            has_generated_data = False
            for sheet_name in check['sheetNames']:
                if sheet_name in COLUMNS and COLUMNS[sheet_name]['generatedData']:
                    has_generated_data = True
                    break
                    
            if not has_generated_data:
                # 生成データが不要な場合は標準のフィールドを設定
                for platform in check['platform']:
                    condition_header = f"{platform}ConditionStatement"
                    check[condition_header] = ""
                    
                check['isSubcheck'] = False
                check['subchecks'] = {}
            else:
                # conditionsがない場合の処理
                if 'conditions' not in check:
                    for platform in check['platform']:
                        condition_header = f"{platform}ConditionStatement"
                        check[condition_header] = ""
                    check['isSubcheck'] = False
                    check['subchecks'] = {}
                else:
                    # conditionStatementsの処理
                    for statement in check.get('conditionStatements', []):
                        column_header = f"{statement['platform']}ConditionStatement"
                        check[column_header] = self.format_statement_summary(statement['summary'])
                        
                    # conditionsの処理
                    for condition in check['conditions']:
                        statement_header = f"{condition['platform']}ConditionStatement"
                        procedures = self.extract_procedures(condition)
                        group_length = len(procedures)
                        
                        if 'subchecks' not in check:
                            check['subchecks'] = {}
                            
                        condition_target = f"{check['target']}{condition['platform'].capitalize()}"
                        condition['target'] = condition_target
                        
                        if condition_target not in check['subchecks']:
                            check['subchecks'][condition_target] = {
                                "count": 0,
                                "conditions": []
                            }
                            
                        check['subchecks'][condition_target]["count"] = group_length
                        
                        if group_length == 1:
                            # 単一の手順の場合
                            proc = procedures[0]
                            check[statement_header] = proc['procedure']
                            tools_header = f"{condition['platform']}Tools"
                            check[tools_header] = [proc['toolLink']]
                            check['isSubcheck'] = False
                        else:
                            # 複数の手順の場合
                            for proc in procedures:
                                statement_header = f"{condition['platform']}ConditionStatement"
                                tools_header = f"{condition['platform']}Tools"
                                
                                subcheck = {
                                    "id": proc['id'],
                                    "checkId": "",
                                    "subcheckId": proc['id'],
                                    "platform": [condition['platform']],
                                    "severity": "",
                                    "target": check['target'],
                                    "sheetNames": [condition_target],
                                    "isSubcheck": True
                                }
                                subcheck[statement_header] = proc['procedure']
                                subcheck[tools_header] = [proc['toolLink']]
                                check['subchecks'][condition_target]["conditions"].append(subcheck)
            
            # チェック情報を記録
            check_id = check['id']
            subchecks_by_target = {}
            
            if 'subchecks' in check:
                for target, subcheck_data in check['subchecks'].items():
                    if isinstance(subcheck_data, dict) and 'count' in subcheck_data:
                        subchecks_by_target[target] = subcheck_data['count']
            
            self.check_info[check_id] = CheckInfo(
                id=check_id,
                is_subcheck=check.get('isSubcheck', False),
                subchecks_by_target=subchecks_by_target
            )
            

            # シートごとにデータを振り分け
            for sheet_name in check['sheetNames']:
                if sheet_name not in processed_data:
                    continue
                    
                processed_data[sheet_name].append(check)
                
                # サブチェックの追加
                if check.get('subchecks') and sheet_name in check['subchecks']:
                    for subcheck in check['subchecks'][sheet_name]['conditions']:
                        processed_data[sheet_name].append(subcheck)
        
        return processed_data

    def format_statement_summary(self, statement: M17nField) -> M17nField:
        """チェック文の要約を整形する"""
        return {
            'ja': f"{statement['ja']}ことを確認する。",
            'en': f"Verify that {statement['en']}."
        }

    def extract_procedures(self, condition: Condition) -> List[Procedure]:
        """条件からチェック手順を抽出する"""
        if condition['type'] == 'simple':
            return [condition['procedure']]
            
        extracted_conditions = []
        for cond in condition['conditions']:
            extracted_conditions.extend(self.extract_procedures(cond))
            
        return extracted_conditions

    def generate_checklist(self, source_data: Dict[str, Any],initialize: bool = False):
        """チェックリストを生成するメイン処理
        
        Args:
            source_data: ソースデータ
            initialize: True の場合、2枚目以降のシートを削除して処理を実行
        """
        if initialize:
            self.initialize_spreadsheet()
            # 既存シートの情報を再読み込み
            self._load_existing_sheets()

        # バージョン情報の更新リクエストを生成して保持
        self.version_update_request = self.create_version_info_request(
            version=source_data.get('version', ''),
            date=source_data.get('date', '')
        )

        processed_data = self.process_source_data(source_data['checks'])
        
        logger.info(f"Available targets: {list(processed_data.keys())}")
        logger.info(f"Processing languages: {LANGS}")

        # 各言語・ターゲットごとにシートを準備
        for lang in LANGS:
            for target_id, translations in TARGET_NAMES.items():
                logger.info(f"Checking {target_id} for {lang}")
                if target_id in processed_data:
                    logger.info(f"Creating sheet for {target_id} in {lang}: {translations[lang]}")
                    self.current_lang = lang
                    self.current_target = target_id  # ここで設定
                    sheet = self.prepare_sheet_structure(
                        target_id=target_id,
                        target_name=translations[lang],
                        lang=lang,
                        checks=processed_data[target_id]
                    )
                    self.sheets[sheet.name] = sheet
        
        # バッチ更新を実行
        self.execute_batch_update()

    def get_headers(self, target_id: str, lang: str) -> List[str]:
        """シートのヘッダー情報を取得する
        
        Args:
            target_id: ターゲット識別子（例：'productWeb'）
            lang: 言語コード（'ja'または'en'）
            
        Returns:
            List[str]: ヘッダーの表示名のリスト
        """
        # ID列
        id_headers = COLUMNS['idCols']
        
        # 生成データ列
        generated_data_headers = COLUMNS[target_id]['generatedData']
        
        # ユーザー入力列
        user_entered_headers = COLUMNS['userEntered']
        
        # プレーンデータ列（共通 + ターゲット固有）
        plain_data_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[target_id]['plainData2']
        ]
        
        # リンクデータ列（ターゲット固有 + 共通）
        link_headers = [
            *COLUMNS[target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]
        
        # すべてのプレーンデータヘッダー（表示順を制御するため）
        all_plain_data_headers = [
            *id_headers,
            *generated_data_headers,
            *user_entered_headers,
            *plain_data_headers
        ]
        
        # すべてのヘッダー
        all_headers = [
            *all_plain_data_headers,
            *link_headers
        ]
        
        # ヘッダーの表示名を取得
        header_strings = []
        for header in all_headers:
            display_name = COLUMN_INFO['name'].get(header, {}).get(lang, header)
            header_strings.append(display_name)
            
        return header_strings

    def get_header_info(self, target_id: str, lang: str) -> Dict[str, List[str]]:
        """ヘッダー情報の詳細を取得する（デバッグやカスタム処理用）
        
        Args:
            target_id: ターゲット識別子
            lang: 言語コード
            
        Returns:
            Dict[str, List[str]]: 種類別のヘッダー情報
        """
        id_headers = COLUMNS['idCols']
        generated_data_headers = COLUMNS[target_id]['generatedData']
        user_entered_headers = COLUMNS['userEntered']
        plain_data_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[target_id]['plainData2']
        ]
        link_headers = [
            *COLUMNS[target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]
        
        all_plain_data_headers = [
            *id_headers,
            *generated_data_headers,
            *user_entered_headers,
            *plain_data_headers
        ]
        
        all_headers = [*all_plain_data_headers, *link_headers]
        
        return {
            'idHeaders': id_headers,
            'generatedDataHeaders': generated_data_headers,
            'userEnteredHeaders': user_entered_headers,
            'plainDataHeaders': plain_data_headers,
            'linkHeaders': link_headers,
            'allPlainDataHeaders': all_plain_data_headers,
            'allHeaders': all_headers
        }

    def prepare_row_data(self, check: Check, target_id: str, lang: str, id_to_row: Dict[str, int]) -> List[CellData]:
        """チェック項目から行データを生成する"""
        header_info = self.get_header_info(target_id, lang)
        row_data: List[CellData] = []
        has_generated_data = bool(COLUMNS[target_id]['generatedData'])

        # ID列の処理
        for header in header_info['idHeaders']:
            row_data.append(CellData(
                value=check[header],
                type=CellType.PLAIN,
                formatting={'numberFormat': {'type': 'TEXT', 'pattern': '0000'}}
            ))

        # 生成データ列の処理
        if header_info['generatedDataHeaders']:
            self.create_formula_for_check(check, target_id, lang, row_data, id_to_row)

        # サブチェックを持つ親チェックかどうかを判定
        has_subchecks = False
        if has_generated_data and not check.get('isSubcheck'):
            if check.get('subchecks') and target_id in check['subchecks']:
                has_subchecks = check['subchecks'][target_id].get('count', 0) > 1

        # ユーザー入力列の処理
        validation_dict = CHECK_RESULTS if has_generated_data else FINAL_CHECK_RESULTS
        validation_values = [validation_dict[key][lang] for key in validation_dict.keys()]
        validation_rule = {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': val} for val in validation_values]
            },
            'strict': True,
            'showCustomUi': True
        }

        for header in header_info['userEnteredHeaders']:
            if header == 'result':
                if has_subchecks:
                    # サブチェックを持つ親チェックの場合は空白＆保護のみ
                    row_data.append(CellData(
                        value="",
                        type=CellType.PLAIN,
                        protection=True,
                        formatting={'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}}
                    ))
                else:
                    # 通常の入力セル
                    row_data.append(CellData(
                        value=validation_dict['unchecked'][lang],
                        type=CellType.PLAIN,
                        validation=validation_rule
                    ))
            else:
                row_data.append(CellData(
                    value='',
                    type=CellType.PLAIN
                ))

        # プレーンデータ列の処理
        for header in header_info['plainDataHeaders']:
            value = check.get(header, '')
            if isinstance(value, dict) and {'ja', 'en'}.intersection(value.keys()):
                value = value.get(lang, value.get('ja', ''))
            row_data.append(CellData(
                value=value or '',
                type=CellType.PLAIN
            ))

        # リンクデータ列の処理
        for header in header_info['linkHeaders']:
            links = check.get(header, [])
            if links:
                row_data.append(self.prepare_rich_text_cell(links, lang))
            else:
                row_data.append(CellData(
                    value='',
                    type=CellType.PLAIN
                ))

        return row_data

    def create_formula_for_check(self, check: Check, target_id: str, lang: str, row_data: List[CellData], id_to_row: Dict[str, int]) -> None:
        """チェック項目の計算式を生成し設定する"""
        is_subcheck = check.get('isSubcheck', False)
        check_id = check.get('id')
        current_row = id_to_row[check_id]

        # 生成データ列の数を取得
        generated_data_count = len(COLUMNS[target_id]['generatedData'])
        if generated_data_count == 0:
            return

        if check.get('conditions'):
            for condition in check['conditions']:
                if condition['target'] == target_id:
                    # 条件式を生成
                    formula = self.get_condition_formula(
                        condition, id_to_row, CHECK_RESULTS, FINAL_CHECK_RESULTS, lang
                    )

                    if not is_subcheck:
                        # 親チェックの場合
                        # 最終結果列（C列）
                        ref_col = f'D{current_row}'
                        row_data.append(CellData(
                            value=f'=IF({ref_col}="","{CHECK_RESULTS["unchecked"][lang]}",{ref_col})',
                            type=CellType.FORMULA,
                            protection=True
                        ))
                        
                        # 計算結果列（D列）
                        row_data.append(CellData(
                            value=formula,
                            type=CellType.FORMULA,
                            protection=True
                        ))
                    else:
                        # サブチェックの場合
                        # 最終結果列（C列）は空セル
                        row_data.append(CellData(
                            value="",
                            type=CellType.PLAIN,
                            protection=True
                        ))
                        
                        # 計算結果列（D列）は親チェックと同じ式を使用
                        # 親チェックのIDを取得
                        parent_id = check_id.split('-')[0]
                        parent_row = id_to_row[parent_id]
                        row_data.append(CellData(
                            value=f'=D{parent_row}',  # 親チェックのD列を参照
                            type=CellType.FORMULA,
                            protection=True
                        ))
                    return

        # 条件がない場合や単純なチェックの場合
        if not is_subcheck:
            # 親チェックの場合
            result_cell = f'E{current_row}'
            calc_cell = f'D{current_row}'
            
            # 最終結果列（C列）
            row_data.append(CellData(
                value=f'=IF(${calc_cell}="","{CHECK_RESULTS["unchecked"][lang]}",${calc_cell})',
                type=CellType.FORMULA,
                protection=True
            ))
            
            # 計算結果列（D列）
            formula = (
                f'=IF(${result_cell}="{CHECK_RESULTS["unchecked"][lang]}", "", '
                f'IF(TO_TEXT(${result_cell})="{CHECK_RESULTS["pass"][lang]}", '
                f'"{FINAL_CHECK_RESULTS["pass"][lang]}", "{FINAL_CHECK_RESULTS["fail"][lang]}"))'
            )
            row_data.append(CellData(
                value=formula,
                type=CellType.FORMULA,
                protection=True
            ))
        else:
            # サブチェックの場合
            # 親チェックのIDを取得
            parent_id = check_id.split('-')[0]
            parent_row = id_to_row[parent_id]
            
            # 最終結果列（C列）は空セル
            row_data.append(CellData(
                value="",
                type=CellType.PLAIN,
                protection=True
            ))
            
            # 計算結果列（D列）は親チェックのD列を参照
            row_data.append(CellData(
                value=f'=D{parent_row}',
                type=CellType.FORMULA,
                protection=True
            ))

    def l10n_string(self, field: Union[str, Dict[str, str], None], lang: str) -> str:
        """多言語フィールドから適切な言語の文字列を取得する

        Args:
            field: 文字列または多言語フィールド
            lang: 言語コード

        Returns:
            str: 選択された言語の文字列
        """
        if field is None:
            return ''
        if isinstance(field, str):
            return field
        if isinstance(field, dict):
            return field.get(lang, field.get('ja', ''))
        return ''

    def apply_basic_formatting(self, sheet_id: int, data_length: int) -> List[Dict]:
        """基本的なシート書式設定を適用する
        
        Args:
            sheet_id: シートID
            data_length: データの行数
            
        Returns:
            List[Dict]: 書式設定のリクエスト
        """
        requests = []
        
        # ヘッダー行の書式設定
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                        'textFormat': {'bold': True},
                        'verticalAlignment': 'MIDDLE',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment,wrapStrategy)'
            }
        })
        
        # 全体のセル書式設定
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': data_length + 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'verticalAlignment': 'TOP',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(verticalAlignment,wrapStrategy)'
            }
        })
        
        # ID列の書式設定
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': data_length + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {'type': 'TEXT', 'pattern': '0000'}
                    }
                },
                'fields': 'userEnteredFormat.numberFormat'
            }
        })
        
        # 列の幅を設定
        for i, width in enumerate(self.get_column_widths()):
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': i,
                        'endIndex': i + 1
                    },
                    'properties': {
                        'pixelSize': width
                    },
                    'fields': 'pixelSize'
                }
            })
        
        # 最初の行を固定
        requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        })
        
        return requests

    def add_conditional_formatting(self, sheet_id: int, data_length: int, lang: str) -> List[Dict]:
        """基本的な条件付き書式を追加する
        
        Args:
            sheet_id: シートID
            data_length: データの行数
            lang: 言語コード
            
        Returns:
            List[Dict]: 条件付き書式のリクエスト
        """
        result_column = self.get_result_column_index()
        requests = []
        
        # PASS（OK）の場合の書式
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': data_length + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['pass'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}
                        }
                    }
                }
            }
        })
        
        # FAIL（NG）の場合の書式
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': data_length + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_EQ',
                            'values': [{'userEnteredValue': CHECK_RESULTS['fail'][lang]}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.96, 'green': 0.80, 'blue': 0.80}
                        }
                    }
                }
            }
        })
        
        return requests

    def get_result_column_index(self) -> int:
        """結果列のインデックスを取得する
        
        Returns:
            int: 結果列のインデックス
        """
        # idCols + generatedDataHeaders の長さが結果列のインデックス
        return len(COLUMNS['idCols']) + len(COLUMNS[self.current_target]['generatedData'])

    def get_column_widths(self) -> List[int]:
        """列幅のリストを取得する
        
        Returns:
            List[int]: 各列の幅（ピクセル単位）
        """
        headers = self.get_header_info(self.current_target, self.current_lang)
        return [
            COLUMN_INFO['width'].get(header, 100)
            for header in headers['allHeaders']
        ]

    def handle_pending_formats(self, response: Dict, pending_formats: Dict) -> List[Dict]:
        """新規作成されたシートに対する書式設定を処理"""
        requests = []
        
        for reply in response.get('replies', []):
            if 'addSheet' in reply:
                sheet_id = reply['addSheet']['properties']['sheetId']
                sheet_title = reply['addSheet']['properties']['title']
                
                if sheet_title in pending_formats:
                    # 言語とターゲットを復元
                    for target_id, translations in TARGET_NAMES.items():
                        if translations[self.current_lang] == sheet_title:
                            self.current_target = target_id
                            break
                    
                    data_length = pending_formats[sheet_title]['data_length']
                    requests.extend(self.prepare_sheet_content(sheet_id, self.sheets[sheet_title]))
                    requests.extend(self.apply_basic_formatting(sheet_id, data_length))
                    # requests.extend(self.add_basic_data_validation(sheet_id, data_length, target_id, self.current_lang))
                    requests.extend(self.add_conditional_formatting(sheet_id, data_length, self.current_lang))
        
        return requests

    def prepare_sheet_content(self, sheet_id: int, sheet: SheetStructure) -> List[Dict]:
        """シートの内容を準備するリクエストを生成"""
        requests = []

        # 必要な行数・列数を計算
        required_rows = len(sheet.data)
        required_columns = len(sheet.data[0]) if sheet.data else 0
        
        # 現在のシートのサイズを取得
        spreadsheet = self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id,
            ranges=[sheet.name],
            includeGridData=False
        ).execute()
        
        grid_properties = None
        for s in spreadsheet['sheets']:
            if s['properties']['title'] == sheet.name:
                grid_properties = s['properties']['gridProperties']
                break
        
        if grid_properties:
            current_row_count = grid_properties.get('rowCount', 1000)
            current_column_count = grid_properties.get('columnCount', 26)
            
            # 1. まず必要なサイズまで行と列を確保
            size_adjustment_requests = self.adjust_sheet_size(
                sheet_id,
                required_rows,
                required_columns,
                current_row_count,
                current_column_count
            )
            
            # サイズ調整が必要な場合は先に実行
            if size_adjustment_requests:
                logger.debug("Executing size adjustment requests")
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': size_adjustment_requests}
                ).execute()
            
            # 2. 既存のコンテンツをクリア
            requests.append({
                'updateCells': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': required_rows,
                        'startColumnIndex': 0,
                        'endColumnIndex': required_columns
                    },
                    'fields': '*'
                }
            })
        
        # 3. 新しいデータを書き込む準備


        # データのサイズを取得
        data_row_count = len(sheet.data)
        data_column_count = len(sheet.data[0]) if sheet.data else 0
        
        # まず全列の非表示設定を解除
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': data_column_count
                },
                'properties': {
                    'hiddenByUser': False
                },
                'fields': 'hiddenByUser'
            }
        })

        # データの更新処理
        for i in range(0, len(sheet.data), 1000):
            chunk = sheet.data[i:i + 1000]
            requests.append({
                'updateCells': {
                    'rows': [
                        {
                            'values': [cell.to_sheets_value() for cell in row]
                        }
                        for row in chunk
                    ],
                    'fields': 'userEnteredValue,userEnteredFormat,textFormatRuns,dataValidation',
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': i,
                        'startColumnIndex': 0
                    }
                }
            })

        # シート名からターゲットIDを取得
        target_id = None
        for tid, names in TARGET_NAMES.items():
            if names[self.current_lang] == sheet.name:
                target_id = tid
                break

        if not target_id:
            logger.warning(f"Could not find target_id for sheet: {sheet.name}")
            return requests

        # GeneratedDataの有無を確認
        has_generated_data = bool(COLUMNS[target_id]['generatedData'])
        
        # シートにサブチェックが存在するか確認
        has_subchecks = False
        for row in sheet.data[1:]:  # ヘッダー行をスキップ
            if row[1].value:  # B列（subcheckId）に値がある
                has_subchecks = True
                break

        logger.debug(f"Sheet {sheet.name}: has_generated_data={has_generated_data}, has_subchecks={has_subchecks}")

        # 列の表示/非表示設定
        if has_generated_data:
            if not has_subchecks:
                # サブチェックがない場合はB～D列を非表示
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 1,  # B列
                            'endIndex': 4     # E列の手前まで
                        },
                        'properties': {
                            'hiddenByUser': True
                        },
                        'fields': 'hiddenByUser'
                    }
                })
            else:
                # サブチェックがある場合はC列のみ非表示
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 2,  # C列
                            'endIndex': 3     # D列の手前まで
                        },
                        'properties': {
                            'hiddenByUser': True
                        },
                        'fields': 'hiddenByUser'
                    }
                })
                
                # A列とB列をマージ
                requests.append({
                    'mergeCells': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 2
                        },
                        'mergeType': 'MERGE_ALL'
                    }
                })
        else:
            # GeneratedDataがない場合はB列を非表示
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 1,  # B列
                        'endIndex': 2     # C列の手前まで
                    },
                    'properties': {
                        'hiddenByUser': True
                    },
                    'fields': 'hiddenByUser'
                }
            })

        # 条件付き書式の設定
        formats = self.get_conditional_formats(target_id, data_row_count, self.current_lang)
        for format_request in formats:
            if 'addConditionalFormatRule' in format_request:
                format_request['addConditionalFormatRule']['rule']['ranges'][0]['sheetId'] = sheet_id
                requests.append(format_request)
        # 保護設定の追加
        data_length = len(sheet.data) if sheet.data else 0
        target_id = None
        
        # シート名からターゲットIDを取得
        for tid, names in TARGET_NAMES.items():
            if names[self.current_lang] == sheet.name:
                target_id = tid
                break
        
        if target_id:
            # 基本的な保護設定を追加
            protection_requests = self.add_protection_requests(sheet_id, data_length, target_id)
            requests.extend(protection_requests)
            
        # サブチェックを持つ親チェックの保護設定
        for i, row in enumerate(sheet.data[1:], start=1):  # ヘッダー行をスキップ
            if self.is_parent_check_with_subchecks(row, target_id):  # target_idを渡す
                parent_protection = self.protect_parent_check_cells(sheet_id, i)
                requests.append(parent_protection)

        return requests

    def adjust_sheet_size(self, sheet_id: int, required_rows: int, required_columns: int, 
                        current_row_count: int, current_column_count: int) -> List[Dict]:
        """シートのサイズを必要な行数・列数に調整する
        
        Args:
            sheet_id: シートID
            required_rows: 必要な行数
            required_columns: 必要な列数
            current_row_count: 現在の行数
            current_column_count: 現在の列数
            
        Returns:
            List[Dict]: サイズ調整のリクエスト
        """
        requests = []
        
        # 行数の調整
        if current_row_count < required_rows:
            # 行数が足りない場合は追加
            requests.append({
                'appendDimension': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'length': required_rows - current_row_count
                }
            })
        elif current_row_count > required_rows:
            # 余分な行がある場合は削除
            requests.append({
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': required_rows,
                        'endIndex': current_row_count
                    }
                }
            })
        
        # 列数の調整
        if current_column_count < required_columns:
            # 列数が足りない場合は追加
            requests.append({
                'appendDimension': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'length': required_columns - current_column_count
                }
            })
        elif current_column_count > required_columns:
            # 余分な列がある場合は削除
            requests.append({
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': required_columns,
                        'endIndex': current_column_count
                    }
                }
            })
        
        if requests:
            logger.debug(
                f"Adjusting sheet size - Required: {required_rows}x{required_columns}, "
                f"Current: {current_row_count}x{current_column_count}"
            )
        
        return requests

    def get_condition_formula(self, cond: Condition, id_to_row: Dict[str, int], check_results: Dict[str, M17nField], final_results: Dict[str, M17nField], lang: str) -> str:
        """条件式を生成する
        
        Args:
            cond: 条件
            id_to_row: ID to 行番号のマッピング
            check_results: チェック結果の文字列定義
            final_results: 最終結果の文字列定義
            lang: 言語コード
            
        Returns:
            str: 条件式
        """
        pass_phrase = check_results['pass'][lang]
        final_pass_phrase = final_results['pass'][lang]
        final_fail_phrase = final_results['fail'][lang]
        
        # 結果の判定式
        pass_formula = self.analyze_condition_formula(cond, id_to_row, pass_phrase)
        # 未チェックの判定式
        unchecked_formula = self.get_unchecked_formula(cond, id_to_row, check_results, lang)
        
        return f'=IF({unchecked_formula},IF({pass_formula},"{final_pass_phrase}","{final_fail_phrase}"))'

    def analyze_condition_formula(self, cond: Condition, id_to_row: Dict[str, int], phrase: str, type_: str = "", operator: str = "=") -> str:
        """条件式の分析部分を生成する
    
        Args:
            cond: 条件
            id_to_row: ID to 行番号のマッピング
            phrase: 比較する文字列
            type_: 条件タイプ（空文字または"reverse"）
            operator: 比較演算子
        
        Returns:
            str: 条件式
        """
        COLUMN = "E"  # 結果列
        
        if cond['type'] == 'simple':
            proc_id = cond['procedure']['id']
            return f'TO_TEXT(${COLUMN}${id_to_row[proc_id]}){operator}"{phrase}"'
        
        # 単純な条件をフィルタリング
        simple_conditions = [
            c for c in cond['conditions']
            if c['type'] == 'simple'
        ]
        # 複合条件をフィルタリング
        complex_conditions = [
            c for c in cond['conditions']
            if c['type'] != 'simple'
        ]
        
        # 条件式の生成
        simple_formulas = [
            self.analyze_condition_formula(c, id_to_row, phrase, type_, operator)
            for c in simple_conditions
        ]
        complex_formulas = [
            self.analyze_condition_formula(c, id_to_row, phrase, type_, operator)
            for c in complex_conditions
        ]
        
        # 関数の選択（AND/OR）
        func = type_ or ('AND' if cond['type'] == 'and' else 'OR')
        if type_ == 'reverse':
            func = 'OR' if cond['type'] == 'and' else 'AND'
        
        all_formulas = simple_formulas + complex_formulas
        return f'{func}({",".join(all_formulas)})'

    def get_unchecked_formula(self, cond: Condition, id_to_row: Dict[str, int], phrases: Dict[str, M17nField], lang: str) -> str:
        """未チェック判定の式を生成する
        
        Args:
            cond: 条件
            id_to_row: ID to 行番号のマッピング
            phrases: チェック結果の文字列定義
            lang: 言語コード
        
        Returns:
            str: 条件式
        """
        unchecked_phrase = phrases['unchecked'][lang]
        COLUMN = "E"  # 結果列
        
        rows = self.get_relevant_rows(cond, id_to_row)
        row_count = len(rows)
        range_ = f'${COLUMN}${rows[0]}:${COLUMN}${rows[row_count - 1]}'
        
        return f'COUNTIF({range_},"{unchecked_phrase}")={row_count},""'

    def get_relevant_rows(self, cond: Condition, id_to_row: Dict[str, int]) -> List[int]:
        """条件に関連する行番号を取得する
        
        Args:
            cond: 条件
            id_to_row: ID to 行番号のマッピング
        
        Returns:
            List[int]: 行番号のリスト
        """
        if cond['type'] == 'simple':
            proc_id = cond['procedure']['id']
            return [id_to_row[proc_id]]
        
        # 再帰的に関連行を収集
        rows = []
        for c in cond['conditions']:
            rows.extend(self.get_relevant_rows(c, id_to_row))
        
        # 行番号でソート
        return sorted(rows)

    def add_protection_requests(self, sheet_id: int, data_length: int, target_id: str) -> List[Dict]:
        """保護設定のリクエストを生成する
        
        Args:
            sheet_id: シートID
            data_length: データの行数
            target_id: ターゲット識別子
            
        Returns:
            List[Dict]: 保護設定のリクエスト
        """
        requests = []
        
        # 生成データ列がある場合の保護設定
        if COLUMNS[target_id]['generatedData']:
            # 生成データ列（C列とD列）の保護
            generated_data_start = len(COLUMNS['idCols'])  # B列の次
            generated_data_count = len(COLUMNS[target_id]['generatedData'])
            
            requests.append({
                'addProtectedRange': {
                    'protectedRange': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 1,  # ヘッダー行の次から
                            'endRowIndex': data_length + 1,
                            'startColumnIndex': generated_data_start,
                            'endColumnIndex': generated_data_start + generated_data_count
                        },
                        'description': 'Generated data protection',
                        'warningOnly': False,
                        'editors': {
                            'domainUsersCanEdit': False  # ドメインユーザーによる編集を禁止
                        }
                    }
                }
            })

        return requests

    def protect_parent_check_cells(self, sheet_id: int, row_index: int) -> Dict:
        """サブチェックを持つ親チェックの入力セルを保護する
        
        Args:
            sheet_id: シートID
            row_index: 行インデックス（0ベース）
            
        Returns:
            Dict: 保護設定のリクエスト
        """
        # 結果入力列（E列）のインデックスを取得
        result_column = self.get_result_column_index()
        
        return {
            'addProtectedRange': {
                'protectedRange': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_index,
                        'endRowIndex': row_index + 1,
                        'startColumnIndex': result_column,
                        'endColumnIndex': result_column + 1
                    },
                    'description': 'Parent check cell protection',
                    'warningOnly': False,
                    'editors': {
                        'domainUsersCanEdit': False
                    }
                }
            }
        }

    def is_parent_check_with_subchecks(self, row: List[CellData], target_id: str) -> bool:
        """特定のターゲットについて、サブチェックを持つ親チェックかどうかを判定する
        
        Args:
            row: 行データ
            target_id: ターゲット識別子（例：'productWeb'）
            
        Returns:
            bool: 指定されたターゲットに対してサブチェックを持つ親チェックの場合True
        """
        # checkIdを取得
        check_id = row[0].value if row[0].value else ""
        
        # チェック情報から判定
        if check_id in self.check_info:
            check_info = self.check_info[check_id]
            if check_info.is_subcheck:
                return False
                
            # 指定されたターゲットに対するサブチェック数を確認
            subcheck_count = check_info.subchecks_by_target.get(target_id, 0)
            return subcheck_count > 1
        
        return False

    def get_first_sheet_id(self) -> int:
        """1枚目のシートのIDを取得する
        
        Returns:
            int: シートID
            
        Raises:
            KeyError: 1枚目のシートの情報が存在しない場合
        """
        first_sheet_name = next(iter(self.existing_sheets))
        sheet_info = self.existing_sheets[first_sheet_name]
        return sheet_info['sheetId']

    def create_version_info_request(self, version: str, date: str) -> Dict:
        """バージョン情報を更新するリクエストを生成する"""
        first_sheet_name = next(iter(self.existing_sheets))
        sheet_id = self.existing_sheets[first_sheet_name]['sheetId']
        logger.debug(f"Creating version info request for sheet {first_sheet_name} (id: {sheet_id})")
        
        # A27セルの位置を計算（0ベースのインデックスに変換）
        row_index = 26  # 27 - 1
        column_index = 0  # A = 0
        
        version_string = f"チェックリスト・バージョン：{version} ({date})"
        logger.debug(f"Version string: {version_string}")
        
        return {
            'updateCells': {
                'rows': [{
                    'values': [{
                        'userEnteredValue': {
                            'stringValue': version_string
                        }
                    }]
                }],
                'fields': 'userEnteredValue',
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': row_index,
                    'endRowIndex': row_index + 1,
                    'startColumnIndex': column_index,
                    'endColumnIndex': column_index + 1
                }
            }
        }

class GoogleAuthManager:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: str = 'credentials.json', 
                 token_path: str = 'token.json'):
        """Google認証マネージャーの初期化
        
        Args:
            credentials_path: クライアントシークレットJSONファイルのパス
            token_path: 認証トークンを保存するパス
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        
    def get_credentials(self) -> Credentials:
        """認証情報を取得する
        
        Returns:
            Credentials: Google API認証情報
            
        Raises:
            FileNotFoundError: 認証情報ファイルが見つからない場合
            Exception: 認証処理に失敗した場合
        """
        creds = None
        
        # 保存されたトークンがあれば読み込み
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
                logger.info("Loaded existing token")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
        
        # トークンが無効な場合の処理
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired token")
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    creds = None
            
            # 新規認証が必要な場合
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download it from GCP Console."
                    )
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, 
                        self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    logger.info("Created new token through authentication flow")
                except Exception as e:
                    logger.error(f"Failed to authenticate: {e}")
                    raise
            
            # 新しいトークンを保存
            try:
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info(f"Saved token to {self.token_path}")
            except Exception as e:
                logger.error(f"Failed to save token: {e}")
                # トークンの保存に失敗しても認証自体は完了しているので続行
                
        return creds

def main():
    try:
        # 認証情報の取得
        auth_manager = GoogleAuthManager()
        credentials = auth_manager.get_credentials()
        
    except FileNotFoundError as e:
        logger.error(f"Authentication error: {e}")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return

    # チェックリストジェネレーターの初期化と実行
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load source data: {e}")
        return
    generator = ChecklistSheetGenerator(credentials, SPREADSHEET_ID)
    generator.generate_checklist(source_data, initialize=False)

if __name__ == '__main__':
    main()

