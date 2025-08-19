from typing import Dict, List, Any
import logging
from .sheet_structure import SheetStructure
from .cell_data import CellData, CellType
from .column_manager import ColumnManager
from .row_data_builder import RowDataBuilder
from .sheet_formatter import SheetFormatter

logger = logging.getLogger(__name__)

class SheetStructureBuilder:
    """Builds sheet structures for checklist generation"""
    
    def __init__(self, editor_email: str = ""):
        """Initialize the builder
        
        Args:
            editor_email: Email address of editor for protected ranges
        """
        self.editor_email = editor_email
    
    def build_sheet_structure(
        self,
        target_id: str,
        target_name: str,
        lang: str,
        checks: List[Dict]
    ) -> SheetStructure:
        """Build complete sheet structure for target
        
        Args:
            target_id: Target identifier
            target_name: Display name of target
            lang: Language code
            checks: List of checks for this target
            
        Returns:
            SheetStructure: Complete sheet structure
        """
        logger.info(f"Building sheet structure: target_id={target_id}, target_name={target_name}, lang={lang}")
        
        # Create sheet structure
        sheet = SheetStructure(name=target_name, sheet_id=None)
        
        # Build header row
        header_row = self._build_header_row(target_id, lang)
        sheet.data.append(header_row)
        
        # Create ID to row mapping
        id_to_row = self._create_id_row_mapping(checks, target_id)
        
        # Build data rows
        row_builder = RowDataBuilder(lang, target_id)
        for check in checks:
            row_data = row_builder.prepare_row_data(check, target_id, lang, id_to_row)
            sheet.data.append(row_data)
        
        # Add conditional formatting
        data_length = len(sheet.data)
        formatter = SheetFormatter(lang, target_id, self.editor_email)
        sheet.conditional_formats.extend(formatter.add_conditional_formatting(sheet.sheet_id, data_length))
        
        return sheet
    
    def _build_header_row(self, target_id: str, lang: str) -> List[CellData]:
        """Build header row for sheet
        
        Args:
            target_id: Target identifier
            lang: Language code
            
        Returns:
            List[CellData]: Header row data
        """
        column_manager = ColumnManager(target_id)
        headers = column_manager.get_header_names(lang)
        
        header_row = []
        for header in headers:
            header_row.append(CellData(
                value=header,
                type=CellType.PLAIN,
                formatting={"textFormat": {"bold": True}}
            ))
        
        return header_row
    
    def _create_id_row_mapping(self, checks: List[Dict], target_id: str) -> Dict[str, int]:
        """Create mapping of IDs to row numbers
        
        Args:
            checks: List of checks
            target_id: Current target identifier
            
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
                    if condition['target'] == target_id:
                        if condition['type'] == 'simple':
                            proc_id = condition['procedure']['id']
                            id_to_row[proc_id] = current_row
                        else:
                            self._map_procedure_ids(condition, id_to_row, current_row)

            # Map subcheck IDs
            subchecks = check.get('subchecks', {}).get(target_id, {})
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
        """Map procedure IDs to rows recursively
        
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
