import logging
from typing import Dict, List, Any, Optional
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config import TARGET_NAMES, LANGS, COLUMN_INFO, CHECK_RESULTS, FINAL_CHECK_RESULTS, COLUMNS
from sheet_structure import SheetStructure, CheckInfo
from cell_data import CellData, CellType
from condition_formatter import ConditionFormatter
from sheet_formatter import SheetFormatter
from data_processor import DataProcessor
from utils import create_version_info_request, adjust_sheet_size

logger = logging.getLogger(__name__)

class ChecklistSheetGenerator:
    """Generates Google Sheets checklists from source data"""
    
    def __init__(self, credentials: Credentials, spreadsheet_id: str):
        """Initialize the generator
        
        Args:
            credentials: Google API credentials
            spreadsheet_id: Target spreadsheet ID
        """
        self.service = build('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id
        self.sheets: Dict[str, SheetStructure] = {}
        self.existing_sheets: Dict[str, Dict[str, Any]] = {}
        self.current_lang: str = 'ja'
        self.current_target: str = ''
        self.data_processor = DataProcessor()
        self._load_existing_sheets()

    def _load_existing_sheets(self) -> None:
        """Load existing sheet information from spreadsheet"""
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

    def initialize_spreadsheet(self) -> None:
        """Initialize spreadsheet by removing extra sheets"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            # Delete sheets after first
            if len(spreadsheet.get('sheets', [])) > 1:
                delete_requests = [
                    {'deleteSheet': {'sheetId': sheet['properties']['sheetId']}}
                    for sheet in spreadsheet['sheets'][1:]
                ]
                
                if delete_requests:
                    self.service.spreadsheets().batchUpdate(
                        spreadsheetId=self.spreadsheet_id,
                        body={'requests': delete_requests}
                    ).execute()
                    logger.info("Deleted existing sheets except the first one")
            
            # Reset existing sheets info
            self.existing_sheets = {
                spreadsheet['sheets'][0]['properties']['title']: {
                    'sheetId': spreadsheet['sheets'][0]['properties']['sheetId'],
                    'index': 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error initializing spreadsheet: {e}")
            raise

    def prepare_sheet_structure(
        self,
        target_id: str,
        target_name: str,
        lang: str,
        checks: List[Dict]
    ) -> SheetStructure:
        """Prepare sheet structure for target
        
        Args:
            target_id: Target identifier
            target_name: Display name of target
            lang: Language code
            checks: List of checks for this target
            
        Returns:
            SheetStructure: Prepared sheet structure
        """
        self.current_lang = lang
        self.current_target = target_id
        
        logger.info(f"Preparing sheet structure: target_id={target_id}, target_name={target_name}, lang={lang}")
        sheet = SheetStructure(name=target_name, sheet_id=None)
        
        # Prepare headers
        headers = self.get_headers(target_id, lang)
        header_row = []
        for header in headers:
            header_row.append(CellData(
                value=header,
                type=CellType.PLAIN,
                formatting={"textFormat": {"bold": True}}
            ))
        sheet.data.append(header_row)
        
        # Map IDs to rows
        id_to_row = self._create_id_row_mapping(checks)
        
        # Prepare data rows
        for check in checks:
            row_data = self.prepare_row_data(check, target_id, lang, id_to_row)
            sheet.data.append(row_data)
        
        # Add conditional formatting
        data_length = len(sheet.data)
        formatter = SheetFormatter(self.current_lang, self.current_target)
        sheet.conditional_formats.extend(formatter.add_conditional_formatting(sheet.sheet_id, data_length))
        
        return sheet

    def get_headers(self, target_id: str, lang: str) -> List[str]:
        """Get column headers for sheet
        
        Args:
            target_id: Target identifier
            lang: Language code
            
        Returns:
            List[str]: Localized header names
        """
        # Column groups in order
        id_headers = COLUMNS['idCols']
        generated_headers = COLUMNS[target_id]['generatedData']
        user_headers = COLUMNS['userEntered']
        plain_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[target_id]['plainData2']
        ]
        link_headers = [
            *COLUMNS[target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]
        
        # All headers in order
        all_headers = [
            *id_headers,
            *generated_headers,
            *user_headers,
            *plain_headers,
            *link_headers
        ]
        
        # Get localized names
        return [
            COLUMN_INFO['name'].get(header, {}).get(lang, header)
            for header in all_headers
        ]

    def prepare_row_data(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        id_to_row: Dict[str, int]
    ) -> List[CellData]:
        """Prepare data for a single row
        
        Args:
            check: Check data to process
            target_id: Target identifier 
            lang: Language code
            id_to_row: Mapping of IDs to row numbers
            
        Returns:
            List[CellData]: List of prepared cell data
        """
        row_data = []
        
        # Add ID columns
        for header in COLUMNS['idCols']:
            row_data.append(CellData(
                value=check[header],
                type=CellType.PLAIN,
                formatting={'numberFormat': {'type': 'TEXT', 'pattern': '0000'}}
            ))
            
        # Add generated data if needed
        if COLUMNS[target_id]['generatedData']:
            self._add_generated_data(check, target_id, lang, row_data, id_to_row)
            
        # Add user entry columns
        self._add_user_entry_columns(check, target_id, lang, row_data)
        
        # Add plain data columns
        self._add_plain_data_columns(check, target_id, lang, row_data)
        
        # Add link columns
        self._add_link_columns(check, target_id, lang, row_data)
        
        return row_data

    def _add_generated_data(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData],
        id_to_row: Dict[str, int]
    ) -> None:
        """Add generated data columns to row
        
        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
            id_to_row: ID to row mapping
        """
        is_subcheck = check.get('isSubcheck', False)
        has_subchecks = (
            not is_subcheck and
            check.get('subchecks') and
            target_id in check['subchecks'] and
            check['subchecks'][target_id].get('count', 0) > 1
        )
        
        formatter = ConditionFormatter(CHECK_RESULTS, FINAL_CHECK_RESULTS)
        
        if check.get('conditions'):
            for condition in check['conditions']:
                if condition['target'] == target_id:
                    formula = formatter.get_condition_formula(condition, id_to_row, lang)
                    
                    if not is_subcheck:
                        # Parent check
                        ref_col = f'D{id_to_row[check["id"]]}'
                        row_data.extend([
                            CellData(
                                value=f'=IF({ref_col}="","{CHECK_RESULTS["unchecked"][lang]}",{ref_col})',
                                type=CellType.FORMULA,
                                protection=True
                            ),
                            CellData(
                                value=formula,
                                type=CellType.FORMULA,
                                protection=True
                            )
                        ])
                    else:
                        # Subcheck
                        parent_id = check['id'].split('-')[0]
                        parent_row = id_to_row[parent_id]
                        row_data.extend([
                            CellData(value="", type=CellType.PLAIN, protection=True),
                            CellData(
                                value=f'=D{parent_row}',
                                type=CellType.FORMULA,
                                protection=True
                            )
                        ])
                    return
                    
        # Simple check case
        if not is_subcheck:
            result_cell = f'E{id_to_row[check["id"]]}'
            calc_cell = f'D{id_to_row[check["id"]]}'
            row_data.extend([
                CellData(
                    value=f'=IF(${calc_cell}="","{CHECK_RESULTS["unchecked"][lang]}",${calc_cell})',
                    type=CellType.FORMULA,
                    protection=True
                ),
                CellData(
                    value=(
                        f'=IF(${result_cell}="{CHECK_RESULTS["unchecked"][lang]}", "", '
                        f'IF(TO_TEXT(${result_cell})="{CHECK_RESULTS["pass"][lang]}", '
                        f'"{FINAL_CHECK_RESULTS["pass"][lang]}", "{FINAL_CHECK_RESULTS["fail"][lang]}"))'
                    ),
                    type=CellType.FORMULA,
                    protection=True
                )
            ])
        else:
            parent_id = check['id'].split('-')[0]
            parent_row = id_to_row[parent_id]
            row_data.extend([
                CellData(value="", type=CellType.PLAIN, protection=True),
                CellData(
                    value=f'=D{parent_row}',
                    type=CellType.FORMULA,
                    protection=True
                )
            ])

    def _add_user_entry_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add user entry columns to row
        
        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        validation_dict = CHECK_RESULTS if COLUMNS[target_id]['generatedData'] else FINAL_CHECK_RESULTS
        validation_values = [validation_dict[key][lang] for key in validation_dict.keys()]
        validation_rule = {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': val} for val in validation_values]
            },
            'strict': True,
            'showCustomUi': True
        }
        
        is_subcheck = check.get('isSubcheck', False)
        has_subchecks = (
            not is_subcheck and
            check.get('subchecks') and
            target_id in check['subchecks'] and
            check['subchecks'][target_id].get('count', 0) > 1
        )
        
        for header in COLUMNS['userEntered']:
            if header == 'result':
                if has_subchecks:
                    row_data.append(CellData(
                        value="",
                        type=CellType.PLAIN,
                        protection=True,
                        formatting={'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}}
                    ))
                else:
                    row_data.append(CellData(
                        value=validation_dict['unchecked'][lang],
                        type=CellType.PLAIN,
                        validation=validation_rule
                    ))
            else:
                row_data.append(CellData(value='', type=CellType.PLAIN))

    def _add_plain_data_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add plain data columns to row
        
        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        from utils import l10n_string
        
        plain_headers = [
            *COLUMNS['common']['plainData1'],
            *COLUMNS[target_id]['plainData1'],
            *COLUMNS['common']['plainData2'],
            *COLUMNS[target_id]['plainData2']
        ]
        
        for header in plain_headers:
            value = check.get(header, '')
            if isinstance(value, dict) and {'ja', 'en'}.intersection(value.keys()):
                value = l10n_string(value, lang)
            row_data.append(CellData(
                value=value or '',
                type=CellType.PLAIN
            ))

    def _add_link_columns(
        self,
        check: Dict,
        target_id: str,
        lang: str,
        row_data: List[CellData]
    ) -> None:
        """Add link columns to row
        
        Args:
            check: Check data
            target_id: Target identifier
            lang: Language code
            row_data: Row data to append to
        """
        link_headers = [
            *COLUMNS[target_id]['linkData'],
            *COLUMNS['common']['linkData']
        ]
        
        for header in link_headers:
            links = check.get(header, [])
            if links:
                row_data.append(self._create_rich_text_cell(links, lang))
            else:
                row_data.append(CellData(value='', type=CellType.PLAIN))

    def _create_rich_text_cell(self, links: List[Dict], lang: str) -> CellData:
        """Create rich text cell with formatted links
        
        Args:
            links: List of link data
            lang: Language code
            
        Returns:
            CellData: Formatted cell data
        """
        text_parts = []
        format_runs = []
        current_index = 0
        
        for i, link in enumerate(links):
            if i > 0:
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
        
        return CellData(
            value={'text': ''.join(text_parts), 'format_runs': format_runs},
            type=CellType.RICH_TEXT
        )

    def _create_id_row_mapping(self, checks: List[Dict]) -> Dict[str, int]:
        """Create mapping of IDs to row numbers
        
        Args:
            checks: List of checks
            
        Returns:
            Dict[str, int]: Mapping of IDs to row numbers
        """
        id_to_row = {}
        current_row = 2  # Start after header
        
        for check in checks:
            if check.get('isSubcheck'):
                continue
                
            check_id = check['id']
            id_to_row[check_id] = current_row
            
            # Map procedure IDs
            if check.get('conditions'):
                for condition in check['conditions']:
                    if condition['target'] == self.current_target:
                        if condition['type'] == 'simple':
                            proc_id = condition['procedure']['id']
                            id_to_row[proc_id] = current_row
                        else:
                            self._map_procedure_ids(condition, id_to_row, current_row)

            # Map subcheck IDs
            subchecks = check.get('subchecks', {}).get(self.current_target, {})
            if subchecks and 'conditions' in subchecks:
                subcheck_count = len(subchecks['conditions'])
                
                for i, subcheck in enumerate(subchecks['conditions'], start=1):
                    subcheck_row = current_row + i
                    id_to_row[subcheck['id']] = subcheck_row
                    
                    if subcheck.get('conditions'):
                        for condition in subcheck['conditions']:
                            if condition['type'] == 'simple':
                                proc_id = condition['procedure']['id']
                                id_to_row[proc_id] = subcheck_row
                            else:
                                self._map_procedure_ids(condition, id_to_row, subcheck_row)
                
                current_row += subcheck_count
                
            current_row += 1

        return id_to_row

    def _map_procedure_ids(
        self,
        condition: Dict,
        id_to_row: Dict[str, int],
        row: int
    ) -> None:
        """Map procedure IDs to rows
        
        Args:
            condition: Condition to process
            id_to_row: ID to row mapping to update
            row: Current row number
        """
        if condition['type'] == 'simple':
            id_to_row[condition['procedure']['id']] = row
        else:
            for cond in condition['conditions']:
                self._map_procedure_ids(cond, id_to_row, row)

    def generate_checklist(self, source_data: Dict[str, Any], initialize: bool = False) -> None:
        """Generate complete checklist
        
        Args:
            source_data: Source data to process
            initialize: Whether to initialize spreadsheet first
        """
        if initialize:
            self.initialize_spreadsheet()
            self._load_existing_sheets()

        # Store version info request
        self.version_update_request = create_version_info_request(
            source_data.get('version', ''),
            source_data.get('date', ''),
            self.get_first_sheet_id()
        )

        # Process source data
        processed_data = self.data_processor.process_source_data(source_data['checks'])
        
        logger.info(f"Available targets: {list(processed_data.keys())}")
        logger.info(f"Processing languages: {LANGS}")

        # Generate sheets for each language and target
        for lang in LANGS:
            for target_id, translations in TARGET_NAMES.items():
                if target_id in processed_data:
                    logger.info(f"Creating sheet for {target_id} in {lang}: {translations[lang]}")
                    self.current_lang = lang
                    self.current_target = target_id
                    sheet = self.prepare_sheet_structure(
                        target_id=target_id,
                        target_name=translations[lang],
                        lang=lang,
                        checks=processed_data[target_id]
                    )
                    self.sheets[sheet.name] = sheet
        
        # Execute updates
        self.execute_batch_update()

    def execute_batch_update(self) -> None:
        """Execute batch update of spreadsheet"""
        try:
            # Initial batch update
            initial_requests, pending_formats = self.generate_batch_requests()
            
            # Execute sheet creation requests
            creation_requests = [req for req in initial_requests if 'addSheet' in req]
            if creation_requests:
                logger.info(f"Creating sheets: {[req.get('addSheet', {}).get('properties', {}).get('title') for req in creation_requests]}")
                creation_response = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': creation_requests}
                ).execute()
                
                # Update sheet IDs
                for reply in creation_response.get('replies', []):
                    if 'addSheet' in reply:
                        sheet_id = reply['addSheet']['properties']['sheetId']
                        sheet_title = reply['addSheet']['properties']['title']
                        self.existing_sheets[sheet_title] = {
                            'sheetId': sheet_id,
                            'index': 0
                        }

            # Generate and execute remaining updates
            update_requests, _ = self.generate_batch_requests()
            update_requests = [req for req in update_requests if 'addSheet' not in req]
            
            if update_requests:
                logger.info(f"Updating {len(update_requests)} sheet contents")
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': update_requests}
                ).execute()
                            
        except Exception as e:
            logger.error(f"Error executing batch update: {e}")
            raise

    def generate_batch_requests(self) -> tuple[List[Dict], Dict]:
        """Generate batch update requests
        
        Returns:
            tuple[List[Dict], Dict]: Requests and pending formats
        """
        requests = []
        pending_formats = {}

        logger.info(f"Generating requests for sheets: {list(self.sheets.keys())}")

        for sheet_name, sheet in self.sheets.items():
            data_length = len(sheet.data)
            column_count = len(sheet.data[0]) if sheet.data else 26

            logger.debug(f"Processing sheet '{sheet_name}', exists: {sheet_name in self.existing_sheets}")

            # Get target ID and language
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

            if target_id is None:
                logger.warning(f"Could not find target_id for sheet: {sheet_name}")
                continue

            # Handle existing or new sheet
            if sheet_name in self.existing_sheets:
                sheet_id = self.existing_sheets[sheet_name]['sheetId']
                logger.debug(f"Updating existing sheet: {sheet_name} (id: {sheet_id})")
                
                formatter = SheetFormatter(current_lang, target_id)
                
                # Clear existing content
                requests.append({
                    'updateCells': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'startColumnIndex': 0
                        },
                        'fields': '*'
                    }
                })
                
                # Add content and formatting
                self._add_sheet_content_requests(requests, sheet_id, sheet)
                requests.extend(formatter.apply_basic_formatting(sheet_id, data_length))
                requests.extend(formatter.add_conditional_formatting(sheet_id, data_length))
            else:
                # Create new sheet
                logger.info(f"Creating new sheet: {sheet_name} with {column_count} columns")
                requests.append({
                    'addSheet': {
                        'properties': {
                            'title': sheet_name,
                            'gridProperties': {
                                'rowCount': max(data_length + 1, 1000),
                                'columnCount': max(column_count, 26)
                            }
                        }
                    }
                })
                
                pending_formats[sheet_name] = {
                    'data_length': data_length,
                    'formats': []
                }

        return requests, pending_formats

    def _add_sheet_content_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        sheet: SheetStructure
    ) -> None:

        data_length = len(sheet.data)
        column_count = len(sheet.data[0]) if sheet.data else 26
        
        try:
            # スプレッドシートの情報を取得
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
                
                # 1. サイズ調整が必要な場合は先に実行
                size_adjustment_requests = adjust_sheet_size(
                    sheet_id,
                    data_length,
                    column_count,
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
                            'endRowIndex': data_length,
                            'startColumnIndex': 0,
                            'endColumnIndex': column_count
                        },
                        'fields': '*'
                    }
                })

            # 3. 新しいデータを書き込む処理...
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

            # 4. 列幅の設定
            for i, width in enumerate(self._get_column_widths()):
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

            # Cell formatting and protection
            formatter = SheetFormatter(self.current_lang, self.current_target)
            data_length = len(sheet.data)
            requests.extend(formatter.apply_basic_formatting(sheet_id, data_length))

            # Add protection settings
            protection_requests = formatter.add_protection_settings(sheet_id, sheet)
            requests.extend(protection_requests)
            
            # Add parent check protection
            for i, row in enumerate(sheet.data[1:], start=1):  # ヘッダー行をスキップ
                if self._is_parent_check_with_subchecks(row):
                    parent_protection = formatter.protect_parent_check_cells(sheet_id, i)
                    requests.append(parent_protection)

            # まず全列の非表示設定を解除
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': column_count
                    },
                    'properties': {
                        'hiddenByUser': False
                    },
                    'fields': 'hiddenByUser'
                }
            })

            # GeneratedDataの有無を確認
            has_generated_data = bool(COLUMNS[self.current_target]['generatedData'])
            
            # シートにサブチェックが存在するか確認
            has_subchecks = False
            for row in sheet.data[1:]:  # ヘッダー行をスキップ
                if row[1].value:  # B列（subcheckId）に値がある
                    has_subchecks = True
                    break

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

        except Exception as e:
            logger.error(f"Error processing sheet content: {e}")
            raise

    def _is_parent_check_with_subchecks(self, row: List[CellData]) -> bool:
        """Check if the row represents a parent check that has subchecks
        
        Args:
            row: Row data
            
        Returns:
            bool: True if this is a parent check with subchecks
        """
        # checkIdを取得
        check_id = row[0].value if row[0].value else ""
        
        # チェック情報から判定
        if check_id in self.data_processor.check_info:
            check_info = self.data_processor.check_info[check_id]
            if check_info.is_subcheck:
                return False
                
            # 指定されたターゲットに対するサブチェック数を確認
            subcheck_count = check_info.subchecks_by_target.get(self.current_target, 0)
            return subcheck_count > 1
        
        return False

    def _get_column_widths(self) -> List[int]:
        """Get list of column widths
        
        Returns:
            List[int]: List of column widths
        """
        headers = self.get_headers(self.current_target, self.current_lang)
        return [
            COLUMN_INFO['width'].get(header, 100)
            for header in headers
        ]

    def get_first_sheet_id(self) -> int:
        """Get ID of first sheet
        
        Returns:
            int: Sheet ID
            
        Raises:
            KeyError: If no sheets exist
        """
        first_sheet_name = next(iter(self.existing_sheets))
        return self.existing_sheets[first_sheet_name]['sheetId']
