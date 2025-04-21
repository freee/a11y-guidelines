from typing import Dict, List, Any
import logging
from .config import TARGET_NAMES, M17nField, COLUMNS
from .sheet_structure import CheckInfo

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processes source checklist data for sheet generation"""
    
    def __init__(self):
        self.check_info: Dict[str, CheckInfo] = {}
    
    def process_source_data(self, src: Dict[str, Any]) -> Dict[str, List[Any]]:
        """Process source data into sheet-ready format
        
        Args:
            src: Raw JSON source data
            
        Returns:
            Dict[str, List[Any]]: Data organized by target
        """
        # Initialize data structure for each target
        processed_data = {target: [] for target in TARGET_NAMES.keys()}
        
        # Sort entries by sortKey
        sorted_entries = sorted(src.items(), key=lambda x: x[1].get('sortKey', 0))
        
        for key, check in sorted_entries:
            # Set basic fields
            check['checkId'] = check['id']
            check['subcheckId'] = ""
            
            # Expand mobile platforms
            if 'mobile' in check['platform']:
                check['platform'].extend(['ios', 'android'])

            # Get sheet names for platforms
            check['sheetNames'] = []
            for platform in check['platform']:
                target_id = f"{check['target']}{platform.capitalize()}"
                if target_id not in TARGET_NAMES:
                    continue
                check['sheetNames'].append(target_id)
                
            # Process generated data requirements
            has_generated_data = self._has_generated_data(check['sheetNames'])
            
            if not has_generated_data:
                # Standard fields for non-generated data
                self._process_standard_fields(check)
            else:
                # Process conditions and subchecks for generated data
                self._process_generated_data_fields(check)
            
            # Record check info
            self._record_check_info(check)
            
            # Distribute to appropriate sheets
            self._distribute_to_sheets(check, processed_data)
        
        return processed_data

    def _has_generated_data(self, sheet_names: List[str]) -> bool:
        """Check if any sheets require generated data
        
        Args:
            sheet_names: List of sheet names to check
            
        Returns:
            bool: True if any sheets require generated data
        """
        return any(
            bool(COLUMNS[name]['generatedData'])
            for name in sheet_names
            if name in COLUMNS
        )

    def _process_standard_fields(self, check: Dict) -> None:
        """Process standard fields for non-generated data
        
        Args:
            check: Check to process
        """
        for platform in check['platform']:
            condition_header = f"{platform}ConditionStatement"
            check[condition_header] = ""
            
        check['isSubcheck'] = False
        check['subchecks'] = {}

    def _process_generated_data_fields(self, check: Dict) -> None:
        """Process fields for checks requiring generated data
        
        Args:
            check: Check to process
        """
        # Handle case with no conditions
        if 'conditions' not in check:
            self._process_standard_fields(check)
            return
            
        # Process condition statements
        for statement in check.get('conditionStatements', []):
            column_header = f"{statement['platform']}ConditionStatement"
            check[column_header] = self._format_statement_summary(statement['summary'])
            
        # Process conditions and subchecks
        for condition in check['conditions']:
            statement_header = f"{condition['platform']}ConditionStatement"
            procedures = self._extract_procedures(condition)
            group_length = len(procedures)
            
            condition_target = f"{check['target']}{condition['platform'].capitalize()}"
            condition['target'] = condition_target
            
            # Initialize subchecks structure
            if 'subchecks' not in check:
                check['subchecks'] = {}
            
            if condition_target not in check['subchecks']:
                check['subchecks'][condition_target] = {
                    "count": 0,
                    "conditions": []
                }
                
            check['subchecks'][condition_target]["count"] = group_length
            
            if group_length == 1:
                # Single procedure case
                proc = procedures[0]
                check[statement_header] = proc['procedure']
                tools_header = f"{condition['platform']}Tools"
                check[tools_header] = [proc['toolLink']]
                check['isSubcheck'] = False
            else:
                # Multiple procedures case
                self._process_multiple_procedures(check, condition, procedures)

    def _format_statement_summary(self, statement: M17nField) -> M17nField:
        """Format check statement summary
        
        Args:
            statement: Statement to format
            
        Returns:
            M17nField: Formatted statement
        """
        return {
            'ja': f"{statement['ja']}ことを確認する。",
            'en': f"Verify that {statement['en']}."
        }

    def _extract_procedures(self, condition: Dict) -> List[Dict]:
        """Extract procedures from condition
        
        Args:
            condition: Condition to extract from
            
        Returns:
            List[Dict]: List of extracted procedures
        """
        if condition['type'] == 'simple':
            return [condition['procedure']]
            
        extracted = []
        for cond in condition['conditions']:
            extracted.extend(self._extract_procedures(cond))
            
        return extracted

    def _process_multiple_procedures(self, check: Dict, condition: Dict, procedures: List[Dict]) -> None:
        """Process multiple procedures for a condition
        
        Args:
            check: Parent check
            condition: Current condition
            procedures: List of procedures to process
        """
        statement_header = f"{condition['platform']}ConditionStatement"
        tools_header = f"{condition['platform']}Tools"
        
        for proc in procedures:
            subcheck = {
                "id": proc['id'],
                "checkId": "",
                "subcheckId": proc['id'],
                "platform": [condition['platform']],
                "severity": "",
                "target": check['target'],
                "sheetNames": [condition['target']],
                "isSubcheck": True
            }
            subcheck[statement_header] = proc['procedure']
            subcheck[tools_header] = [proc['toolLink']]
            check['subchecks'][condition['target']]["conditions"].append(subcheck)

    def _record_check_info(self, check: Dict) -> None:
        """Record check information
        
        Args:
            check: Check to record info for
        """
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

    def _distribute_to_sheets(self, check: Dict, processed_data: Dict[str, List]) -> None:
        """Distribute check data to appropriate sheets
        
        Args:
            check: Check to distribute
            processed_data: Target sheet data
        """
        for sheet_name in check['sheetNames']:
            if sheet_name not in processed_data:
                continue
                
            processed_data[sheet_name].append(check)
            
            # Add subchecks if present
            if check.get('subchecks') and sheet_name in check['subchecks']:
                for subcheck in check['subchecks'][sheet_name]['conditions']:
                    processed_data[sheet_name].append(subcheck)
