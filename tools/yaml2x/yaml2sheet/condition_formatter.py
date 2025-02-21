from typing import Dict, List
from config import M17nField, Condition

class ConditionFormatter:
    """Handles creation and formatting of conditional formulas for sheet cells"""
    
    def __init__(self, check_results: Dict[str, M17nField], final_results: Dict[str, M17nField]):
        """Initialize with result string definitions
        
        Args:
            check_results: Check result string definitions by language
            final_results: Final result string definitions by language
        """
        self.check_results = check_results
        self.final_results = final_results
        self.RESULT_COLUMN = "E"  # Column for result entries
    
    def get_condition_formula(self, cond: Condition, id_to_row: Dict[str, int], lang: str) -> str:
        """Generate formula for condition evaluation
        
        Args:
            cond: Condition to evaluate
            id_to_row: Mapping of IDs to row numbers
            lang: Language code for result strings
            
        Returns:
            str: Excel formula for condition evaluation
        """
        pass_phrase = self.check_results['pass'][lang]
        final_pass_phrase = self.final_results['pass'][lang]
        final_fail_phrase = self.final_results['fail'][lang]
        
        # Check result formula
        pass_formula = self.analyze_condition_formula(cond, id_to_row, pass_phrase)
        # Unchecked state formula
        unchecked_formula = self.get_unchecked_formula(cond, id_to_row, lang)
        
        return f'=IF({unchecked_formula},IF({pass_formula},"{final_pass_phrase}","{final_fail_phrase}"))'

    def analyze_condition_formula(
        self, 
        cond: Condition, 
        id_to_row: Dict[str, int], 
        phrase: str, 
        type_: str = "", 
        operator: str = "="
    ) -> str:
        """Generate analysis part of condition formula
        
        Args:
            cond: Condition to analyze
            id_to_row: Mapping of IDs to row numbers
            phrase: Comparison phrase
            type_: Condition type (empty or "reverse")
            operator: Comparison operator
            
        Returns:
            str: Formula for condition analysis
        """
        if cond['type'] == 'simple':
            proc_id = cond['procedure']['id']
            return f'TO_TEXT(${self.RESULT_COLUMN}${id_to_row[proc_id]}){operator}"{phrase}"'
        
        # Filter simple and complex conditions
        simple_conditions = [c for c in cond['conditions'] if c['type'] == 'simple']
        complex_conditions = [c for c in cond['conditions'] if c['type'] != 'simple']
        
        # Generate formulas
        simple_formulas = [
            self.analyze_condition_formula(c, id_to_row, phrase, type_, operator)
            for c in simple_conditions
        ]
        complex_formulas = [
            self.analyze_condition_formula(c, id_to_row, phrase, type_, operator)
            for c in complex_conditions
        ]
        
        # Select function based on type
        func = type_ or ('AND' if cond['type'] == 'and' else 'OR')
        if type_ == 'reverse':
            func = 'OR' if cond['type'] == 'and' else 'AND'
        
        all_formulas = simple_formulas + complex_formulas
        return f'{func}({",".join(all_formulas)})'

    def get_unchecked_formula(self, cond: Condition, id_to_row: Dict[str, int], lang: str) -> str:
        """Generate formula for checking unchecked state
        
        Args:
            cond: Condition to check
            id_to_row: Mapping of IDs to row numbers
            lang: Language code for result strings
            
        Returns:
            str: Formula for unchecked state
        """
        unchecked_phrase = self.check_results['unchecked'][lang]
        rows = self.get_relevant_rows(cond, id_to_row)
        row_count = len(rows)
        range_ = f'${self.RESULT_COLUMN}${rows[0]}:${self.RESULT_COLUMN}${rows[row_count - 1]}'
        
        return f'COUNTIF({range_},"{unchecked_phrase}")={row_count},""'

    def get_relevant_rows(self, cond: Condition, id_to_row: Dict[str, int]) -> List[int]:
        """Get row numbers relevant to a condition
        
        Args:
            cond: Condition to analyze
            id_to_row: Mapping of IDs to row numbers
            
        Returns:
            List[int]: List of relevant row numbers
        """
        if cond['type'] == 'simple':
            proc_id = cond['procedure']['id']
            return [id_to_row[proc_id]]
        
        # Recursively collect rows
        rows = []
        for c in cond['conditions']:
            rows.extend(self.get_relevant_rows(c, id_to_row))
        
        # Sort by row number
        return sorted(rows)
