import logging
from typing import Dict, List, Any, Optional
import json
from google.oauth2.credentials import Credentials
# Import build for backward compatibility with tests
from googleapiclient.discovery import build

from .config import TARGET_NAMES, LANGS, COLUMN_INFO, CHECK_RESULTS, FINAL_CHECK_RESULTS, COLUMNS
from .config_loader import ApplicationConfig
from .sheet_structure import SheetStructure, CheckInfo
from .cell_data import CellData, CellType
from .condition_formatter import ConditionFormatter
from .sheet_formatter import SheetFormatter
from .data_processor import DataProcessor
from .sheet_api_client import SheetsAPIClient
from .spreadsheet_manager import SpreadsheetManager
from .row_data_builder import RowDataBuilder
from .column_manager import ColumnManager
from .sheet_content_manager import SheetContentManager
from .batch_update_manager import BatchUpdateManager
from .utils import create_version_info_request, adjust_sheet_size
from .sheet_structure_builder import SheetStructureBuilder

logger = logging.getLogger(__name__)

class ChecklistSheetGenerator:
    """Generates Google Sheets checklists from source data"""
    
    def __init__(self, credentials: Credentials, spreadsheet_id: str, 
                 editor_email: str = "", config: Optional[ApplicationConfig] = None):
        """Initialize the generator
        
        Args:
            credentials: Google API credentials
            spreadsheet_id: Target spreadsheet ID
            editor_email: Email address of editor for protected ranges
            config: Application configuration (optional)
        """
        # Store initialization parameters
        self.credentials = credentials
        self.spreadsheet_id = spreadsheet_id
        self.editor_email = editor_email
        self.config = config
        
        # Initialize new architecture components
        self.api_client = SheetsAPIClient(credentials, spreadsheet_id)
        self.spreadsheet_manager = SpreadsheetManager(self.api_client)
        
        # Backward compatibility: expose service at top level
        self.service = self.api_client.service
        
        # For backward compatibility with tests that expect immediate API calls during init,
        # we need to trigger the loading of existing sheets if the service creation succeeded
        # This ensures that any API errors during sheet loading are raised during initialization
        try:
            # Try to access existing_sheets property to trigger loading
            _ = self.existing_sheets
        except Exception:
            # If there's an error loading sheets, re-raise it to maintain test compatibility
            raise
        
        # Initialize other attributes
        self.sheets: Dict[str, SheetStructure] = {}
        self.current_lang: str = 'ja'
        self.current_target: str = ''
        self.data_processor = DataProcessor()

    @property
    def existing_sheets(self) -> Dict[str, Dict[str, Any]]:
        """Backward compatibility: expose existing_sheets from spreadsheet_manager"""
        self.spreadsheet_manager._ensure_sheets_loaded()
        return self.spreadsheet_manager.existing_sheets

    @existing_sheets.setter
    def existing_sheets(self, value: Dict[str, Dict[str, Any]]) -> None:
        """Backward compatibility: allow setting existing_sheets for tests"""
        self.spreadsheet_manager.existing_sheets = value
        self.spreadsheet_manager._sheets_loaded = True

    @property
    def protected_ranges(self) -> Dict[int, List[int]]:
        """Backward compatibility: expose protected_ranges from spreadsheet_manager"""
        self.spreadsheet_manager._ensure_sheets_loaded()
        return self.spreadsheet_manager.protected_ranges

    @protected_ranges.setter
    def protected_ranges(self, value: Dict[int, List[int]]) -> None:
        """Backward compatibility: allow setting protected_ranges for tests"""
        self.spreadsheet_manager.protected_ranges = value

    def initialize_spreadsheet(self) -> None:
        """Initialize spreadsheet by removing extra sheets"""
        self.spreadsheet_manager.initialize_spreadsheet()

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
        
        # Use the new SheetStructureBuilder
        builder = SheetStructureBuilder(self.editor_email)
        return builder.build_sheet_structure(target_id, target_name, lang, checks)

    def get_header_ids(self, target_id: str) -> List[str]:
        """Get column IDs for sheet
        
        Args:
            target_id: Target identifier
            
        Returns:
            List[str]: Column IDs
        """
        column_manager = ColumnManager(target_id)
        return column_manager.get_header_ids()

    def get_header_names(self, target_id: str, lang: str) -> List[str]:
        """Get localized column header names for sheet
        
        Args:
            target_id: Target identifier
            lang: Language code
            
        Returns:
            List[str]: Localized header names
        """
        column_manager = ColumnManager(target_id)
        return column_manager.get_header_names(lang)

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
        # Use the new RowDataBuilder
        row_builder = RowDataBuilder(lang, target_id)
        return row_builder.prepare_row_data(check, target_id, lang, id_to_row)

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
        
        formatter = ConditionFormatter(CHECK_RESULTS, FINAL_CHECK_RESULTS, target_id)
        
        # Calculate column for calculatedResult (second generatedData column) - define once for all cases
        calc_col = chr(ord('A') + len(COLUMNS['idCols']) + 1)  # +1 for finalResult
        
        if check.get('conditions'):
            for condition in check['conditions']:
                if condition['target'] == target_id:
                    formula = formatter.get_condition_formula(condition, id_to_row, lang)
                    
                    if not is_subcheck:
                        # Parent check
                        ref_col = f'{calc_col}{id_to_row[check["id"]]}'
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
                                value=f'={calc_col}{parent_row}',
                                type=CellType.FORMULA,
                                protection=True
                            )
                        ])
                    return
                    
        # Simple check case
        if not is_subcheck:
            # Calculate result column position
            result_col = chr(ord('A') + len(COLUMNS['idCols']) + len(COLUMNS[target_id]['generatedData']))
            result_cell = f'{result_col}{id_to_row[check["id"]]}'
            calc_cell = f'{calc_col}{id_to_row[check["id"]]}'
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
            # Subcheck case
            parent_id = check['id'].split('-')[0]
            parent_row = id_to_row[parent_id]
            row_data.extend([
                CellData(value="", type=CellType.PLAIN, protection=True),
                CellData(
                    value=f'={calc_col}{parent_row}',
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
        from .utils import l10n_string
        
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
            
            url = link['url'][lang]
            # Check if URL is relative and needs base_url
            if url.startswith('/'):
                from freee_a11y_gl import settings as GL
                base_url = GL.get('base_url', '')
                url = base_url.rstrip('/') + url
            
            format_runs.append({
                'startIndex': current_index,
                'format': {
                    'link': {'uri': url},
                    'foregroundColor': {'red': 0.06, 'green': 0.47, 'blue': 0.82},
                    'underline': True
                }
            })
            current_index += len(link_text)
        
        return CellData(
            value={'text': ''.join(text_parts), 'format_runs': format_runs},
            type=CellType.RICH_TEXT
        )


    def generate_checklist(self, source_data: Dict[str, Any], initialize: bool = False) -> None:
        """Generate complete checklist with progress reporting
        
        Args:
            source_data: Source data to process
            initialize: Whether to initialize spreadsheet first
        """
        if initialize:
            logger.info("Initializing spreadsheet (removing existing sheets)")
            self.initialize_spreadsheet()

        # Store version info for later use
        self._version_info = {
            'version': source_data.get('version', ''),
            'date': source_data.get('date', '')
        }
        logger.info(f"Checklist version: {self._version_info['version']} ({self._version_info['date']})")

        # Process source data
        logger.info("Processing source data")
        processed_data = self.data_processor.process_source_data(source_data['checks'])
        
        # Count total sheets to be generated for progress reporting
        total_sheets = 0
        for target_id in processed_data:
            if target_id in TARGET_NAMES:
                total_sheets += len(LANGS)
        
        logger.info(f"Will generate {total_sheets} sheets ({len(processed_data)} targets × {len(LANGS)} languages)")

        # Generate sheets for each language and target
        sheets_processed = 0
        for lang in LANGS:
            for target_id, translations in TARGET_NAMES.items():
                if target_id in processed_data:
                    sheets_processed += 1
                    logger.info(f"Creating sheet {sheets_processed}/{total_sheets}: {target_id} in {lang} ({translations[lang]})")
                    
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
        logger.info("All sheets prepared, executing batch update")
        self.execute_batch_update()
        logger.info("Checklist generation completed successfully")

    def execute_batch_update(self) -> None:
        """Execute batch update of spreadsheet with improved chunking for timeout prevention"""
        try:
            # Initial batch update
            initial_requests, pending_formats = self.generate_batch_requests()
            
            # Execute sheet creation requests
            self._execute_sheet_creation_requests(initial_requests)

            # Generate and execute remaining updates
            self._execute_sheet_update_requests()
                                
        except Exception as e:
            logger.error(f"Error executing batch update: {e}")
            raise

    def _execute_sheet_creation_requests(self, initial_requests: List[Dict]) -> None:
        """Execute sheet creation requests and update sheet IDs
        
        Args:
            initial_requests: List of all initial requests
        """
        creation_requests = [req for req in initial_requests if 'addSheet' in req]
        if not creation_requests:
            return
            
        logger.info(f"Creating sheets: {[req.get('addSheet', {}).get('properties', {}).get('title') for req in creation_requests]}")
        creation_response = self.api_client.batch_update(creation_requests)
        
        # Update sheet IDs
        for reply in creation_response.get('replies', []):
            if 'addSheet' in reply:
                sheet_id = reply['addSheet']['properties']['sheetId']
                sheet_title = reply['addSheet']['properties']['title']
                self.spreadsheet_manager.update_sheet_info(sheet_title, sheet_id, 0)

    def _execute_sheet_update_requests(self) -> None:
        """Execute sheet update requests in batches"""
        update_requests, _ = self.generate_batch_requests()
        update_requests = [req for req in update_requests if 'addSheet' not in req]
        
        if not update_requests:
            return
            
        # Add version info request
        self._add_version_info_request(update_requests)
        
        # Process in smaller batches to avoid timeouts
        self._process_update_batches(update_requests)

    def _add_version_info_request(self, update_requests: List[Dict]) -> None:
        """Add version info request if version info is available
        
        Args:
            update_requests: List of update requests to append to
        """
        if hasattr(self, '_version_info') and hasattr(self, 'config') and self.config:
            first_sheet_id = self.get_first_sheet_id()
            row_index, column_index = self.config.parse_version_info_cell()
            version_update_request = create_version_info_request(
                self._version_info['version'],
                self._version_info['date'],
                first_sheet_id,
                row_index=row_index,
                column_index=column_index
            )
            update_requests.append(version_update_request)
        elif hasattr(self, '_version_info'):
            # Fallback to default behavior if no config is provided
            first_sheet_id = self.get_first_sheet_id()
            version_update_request = create_version_info_request(
                self._version_info['version'],
                self._version_info['date'],
                first_sheet_id
            )
            update_requests.append(version_update_request)

    def _process_update_batches(self, update_requests: List[Dict]) -> None:
        """Process update requests in batches to avoid timeouts
        
        Args:
            update_requests: List of update requests to process
        """
        BATCH_SIZE = 50  # Reduced batch size to avoid timeout
        total_requests = len(update_requests)
        logger.info(f"Updating {total_requests} sheet contents in smaller batches")
        
        # タイムアウト回避のためのバッチ処理
        for i in range(0, total_requests, BATCH_SIZE):
            end_idx = min(i + BATCH_SIZE, total_requests)
            batch = update_requests[i:end_idx]
            batch_num = i//BATCH_SIZE + 1
            total_batches = (total_requests-1)//BATCH_SIZE + 1
            
            logger.info(f"Processing batch {batch_num}/{total_batches}: requests {i+1}-{end_idx} of {total_requests}")
            
            try:
                # タイムアウト設定を長めに
                self.api_client.batch_update(batch)
                logger.info(f"Batch {batch_num} completed successfully")
            except Exception as e:
                logger.error(f"Error in batch {batch_num}: {e}")
                # エラーが発生しても次のバッチを続行
        
        logger.info(f"All sheet updates completed")

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

            logger.debug(f"Processing sheet '{sheet_name}', exists: {self.spreadsheet_manager.sheet_exists(sheet_name)}")

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
            if self.spreadsheet_manager.sheet_exists(sheet_name):
                sheet_id = self.spreadsheet_manager.get_sheet_id(sheet_name)
                logger.debug(f"Updating existing sheet: {sheet_name} (id: {sheet_id})")
                
                formatter = SheetFormatter(current_lang, target_id, self.editor_email)

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
        """Add requests to update sheet content and formatting
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            sheet: Sheet structure containing data and format info
        """
        try:
            data_length = len(sheet.data)
            column_count = len(sheet.data[0]) if sheet.data else 26

            # Get current sheet properties and adjust size if needed
            self._adjust_sheet_size(sheet_id, sheet.name, data_length, column_count)
            
            # Clear existing content
            self._add_clear_content_request(requests, sheet_id, data_length, column_count)
            
            # Add new data in chunks
            self._add_data_update_requests(requests, sheet_id, sheet.data)
            
            # Set column widths
            self._add_column_width_requests(requests, sheet_id)
            
            # Add formatting and protection
            self._add_formatting_requests(requests, sheet_id, sheet, data_length)
            
            # Configure column visibility
            self._add_column_visibility_requests(requests, sheet_id, sheet.data, column_count)

        except Exception as e:
            logger.error(f"Error processing sheet content: {e}")
            raise

    def _adjust_sheet_size(self, sheet_id: int, sheet_name: str, data_length: int, column_count: int) -> None:
        """Adjust sheet size if needed"""
        grid_properties = self.spreadsheet_manager.get_sheet_grid_properties(sheet_name)
                
        if grid_properties:
            current_rows = grid_properties.get('rowCount', 1000)
            current_cols = grid_properties.get('columnCount', 26)
            
            size_requests = adjust_sheet_size(
                sheet_id, data_length, column_count, 
                current_rows, current_cols
            )
            
            if size_requests:
                logger.debug("Executing size adjustment requests")
                self.api_client.batch_update(size_requests)

    def _add_clear_content_request(
        self,
        requests: List[Dict],
        sheet_id: int,
        data_length: int,
        column_count: int
    ) -> None:
        """Add request to clear existing content and remove protected ranges
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            data_length: Number of data rows
            column_count: Number of columns
        """
        # 既存の保護範囲を削除するリクエストを追加
        if hasattr(self, 'protected_ranges') and sheet_id in self.protected_ranges:
            for protected_range_id in self.protected_ranges.get(sheet_id, []):
                requests.append({
                    'deleteProtectedRange': {
                        'protectedRangeId': protected_range_id
                    }
                })
            logger.debug(f"Added requests to delete {len(self.protected_ranges.get(sheet_id, []))} protected ranges from sheet {sheet_id}")
        
        # 既存のセル内容をクリアするリクエスト
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

    def _add_data_update_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        data: List[List[CellData]]
    ) -> None:
        """Add requests to update sheet data in chunks with improved batching
        
        Args:
            requests: List to append requests to
            sheet_id: ID of sheet to update
            data: Data to update
        """
        # Use smaller chunks for better reliability
        CHUNK_SIZE = 100  # Reduced from 1000 to avoid timeouts
        
        total_rows = len(data)
        logger.debug(f"Adding data update requests for {total_rows} rows in chunks of {CHUNK_SIZE}")
        
        for i in range(0, total_rows, CHUNK_SIZE):
            chunk = data[i:i + CHUNK_SIZE]
            end_idx = min(i + CHUNK_SIZE, total_rows)
            logger.debug(f"Processing rows {i+1}-{end_idx} of {total_rows}")
            
            requests.append({
                'updateCells': {
                    'rows': [
                        {'values': [cell.to_sheets_value() for cell in row]}
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

    def _add_column_width_requests(self, requests: List[Dict], sheet_id: int) -> None:
        """Add requests to set column widths"""
        for i, width in enumerate(self._get_column_widths()):
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': i,
                        'endIndex': i + 1
                    },
                    'properties': {'pixelSize': width},
                    'fields': 'pixelSize'
                }
            })

    def _add_formatting_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        sheet: SheetStructure,
        data_length: int
    ) -> None:
        """Add formatting and protection requests"""
        formatter = SheetFormatter(self.current_lang, self.current_target, self.editor_email)
        
        # Basic formatting
        requests.extend(formatter.apply_basic_formatting(sheet_id, data_length))
        
        # Protection settings
        requests.extend(formatter.add_protection_settings(sheet_id, sheet))
        
        # Parent check protection
        for i, row in enumerate(sheet.data[1:], start=1):
            if self._is_parent_check_with_subchecks(row):
                requests.append(formatter.protect_parent_check_cells(sheet_id, i))

    def _add_column_visibility_requests(
        self,
        requests: List[Dict],
        sheet_id: int,
        data: List[List[CellData]],
        column_count: int
    ) -> None:
        """Add requests to configure column visibility"""
        # Reset all column visibility
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': column_count
                },
                'properties': {'hiddenByUser': False},
                'fields': 'hiddenByUser'
            }
        })
        
        has_generated_data = bool(COLUMNS[self.current_target]['generatedData'])
        has_subchecks = any(row[1].value for row in data[1:])  # Check B column after header
        
        if has_generated_data:
            if not has_subchecks:
                # Hide columns B-D if no subchecks
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 1,
                            'endIndex': 4
                        },
                        'properties': {'hiddenByUser': True},
                        'fields': 'hiddenByUser'
                    }
                })
            else:
                # Hide column C and merge A-B for subchecks
                requests.append({
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 2,
                            'endIndex': 3
                        },
                        'properties': {'hiddenByUser': True},
                        'fields': 'hiddenByUser'
                    }
                })
                
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
            # Hide column B if no generated data
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 1,
                        'endIndex': 2
                    },
                    'properties': {'hiddenByUser': True},
                    'fields': 'hiddenByUser'
                }
            })

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
        headers = self.get_header_ids(self.current_target)
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
        return self.spreadsheet_manager.get_first_sheet_id()

    # Backward compatibility methods for tests
    def _create_id_row_mapping(self, checks: List[Dict]) -> Dict[str, int]:
        """Create mapping of IDs to row numbers (backward compatibility)
        
        Args:
            checks: List of checks
            
        Returns:
            Dict[str, int]: Mapping of IDs to row numbers
        """
        builder = SheetStructureBuilder(self.editor_email)
        return builder._create_id_row_mapping(checks, self.current_target)

    def _map_procedure_ids(
        self,
        condition: Dict,
        id_to_row: Dict[str, int],
        row: int
    ) -> None:
        """Map procedure IDs to rows (backward compatibility)
        
        Args:
            condition: Condition to process
            id_to_row: ID to row mapping to update
            row: Current row number
        """
        builder = SheetStructureBuilder(self.editor_email)
        builder._map_procedure_ids(condition, id_to_row, row)
