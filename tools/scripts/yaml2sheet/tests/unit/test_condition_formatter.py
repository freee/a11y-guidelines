"""Tests for condition_formatter module."""

import pytest
from unittest.mock import patch, MagicMock
from yaml2sheet.condition_formatter import ConditionFormatter


class TestConditionFormatter:
    """Test cases for ConditionFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.check_results = {
            'pass': {'ja': '適合', 'en': 'Pass'},
            'fail': {'ja': '不適合', 'en': 'Fail'},
            'unchecked': {'ja': '未確認', 'en': 'Unchecked'}
        }
        self.final_results = {
            'pass': {'ja': '最終適合', 'en': 'Final Pass'},
            'fail': {'ja': '最終不適合', 'en': 'Final Fail'}
        }
        self.target_id = 'design'
        
        # Mock COLUMNS configuration
        self.mock_columns = {
            'idCols': ['A', 'B'],  # 2 columns
            'design': {
                'generatedData': ['C', 'D', 'E']  # 3 columns
            }
        }
        
    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_init_basic(self, mock_columns):
        """Test basic initialization."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        assert formatter.check_results == self.check_results
        assert formatter.final_results == self.final_results
        # Result column should be at index 2 + 3 = 5, which is 'F'
        assert formatter.RESULT_COLUMN == 'F'

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_init_different_target_id(self, mock_columns):
        """Test initialization with different target ID."""
        mock_columns_data = {
            'idCols': ['A'],  # 1 column
            'product': {
                'generatedData': ['B', 'C']  # 2 columns
            }
        }
        mock_columns.__getitem__.side_effect = mock_columns_data.__getitem__
        mock_columns.__contains__.side_effect = mock_columns_data.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            'product'
        )
        
        # Result column should be at index 1 + 2 = 3, which is 'D'
        assert formatter.RESULT_COLUMN == 'D'

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_init_missing_target_id(self, mock_columns):
        """Test initialization with missing target ID."""
        mock_columns_data = {
            'idCols': ['A', 'B', 'C']  # 3 columns
        }
        mock_columns.__getitem__.side_effect = mock_columns_data.__getitem__
        mock_columns.__contains__.return_value = False
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            'nonexistent'
        )
        
        # Result column should be at index 3 + 0 = 3, which is 'D'
        assert formatter.RESULT_COLUMN == 'D'

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_condition_formula_simple(self, mock_columns):
        """Test get_condition_formula with simple condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 10}
        
        result = formatter.get_condition_formula(condition, id_to_row, 'ja')
        
        # Should contain the expected formula structure
        assert 'IF(' in result
        assert '適合' in result
        assert '最終適合' in result
        assert '最終不適合' in result
        assert '$F$10' in result

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_condition_formula_english(self, mock_columns):
        """Test get_condition_formula with English language."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 5}
        
        result = formatter.get_condition_formula(condition, id_to_row, 'en')
        
        assert 'Pass' in result
        assert 'Final Pass' in result
        assert 'Final Fail' in result
        assert '$F$5' in result

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_analyze_condition_formula_simple(self, mock_columns):
        """Test analyze_condition_formula with simple condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 15}
        
        result = formatter.analyze_condition_formula(condition, id_to_row, '適合')
        
        expected = 'TO_TEXT($F$15)="適合"'
        assert result == expected

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_analyze_condition_formula_and_condition(self, mock_columns):
        """Test analyze_condition_formula with AND condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'and',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc1'}
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc2'}
                }
            ]
        }
        id_to_row = {'proc1': 10, 'proc2': 11}
        
        result = formatter.analyze_condition_formula(condition, id_to_row, 'Pass')
        
        assert result.startswith('AND(')
        assert 'TO_TEXT($F$10)="Pass"' in result
        assert 'TO_TEXT($F$11)="Pass"' in result

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_analyze_condition_formula_or_condition(self, mock_columns):
        """Test analyze_condition_formula with OR condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'or',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc1'}
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc2'}
                }
            ]
        }
        id_to_row = {'proc1': 5, 'proc2': 6}
        
        result = formatter.analyze_condition_formula(condition, id_to_row, 'Pass')
        
        assert result.startswith('OR(')
        assert 'TO_TEXT($F$5)="Pass"' in result
        assert 'TO_TEXT($F$6)="Pass"' in result

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_analyze_condition_formula_reverse_type(self, mock_columns):
        """Test analyze_condition_formula with reverse type."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'and',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc1'}
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc2'}
                }
            ]
        }
        id_to_row = {'proc1': 10, 'proc2': 11}
        
        result = formatter.analyze_condition_formula(condition, id_to_row, 'Pass', 'reverse')
        
        # Reverse of AND should be OR
        assert result.startswith('OR(')

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_analyze_condition_formula_custom_operator(self, mock_columns):
        """Test analyze_condition_formula with custom operator."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 8}
        
        result = formatter.analyze_condition_formula(condition, id_to_row, 'Pass', '', '<>')
        
        expected = 'TO_TEXT($F$8)<>"Pass"'
        assert result == expected

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_unchecked_formula(self, mock_columns):
        """Test get_unchecked_formula."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 12}
        
        result = formatter.get_unchecked_formula(condition, id_to_row, 'ja')
        
        expected = 'COUNTIF($F$12:$F$12,"未確認")=1,""'
        assert result == expected

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_unchecked_formula_multiple_rows(self, mock_columns):
        """Test get_unchecked_formula with multiple rows."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'and',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc1'}
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc2'}
                }
            ]
        }
        id_to_row = {'proc1': 10, 'proc2': 15}
        
        result = formatter.get_unchecked_formula(condition, id_to_row, 'en')
        
        expected = 'COUNTIF($F$10:$F$15,"Unchecked")=2,""'
        assert result == expected

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_relevant_rows_simple(self, mock_columns):
        """Test get_relevant_rows with simple condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'simple',
            'procedure': {'id': 'proc1'}
        }
        id_to_row = {'proc1': 20}
        
        result = formatter.get_relevant_rows(condition, id_to_row)
        
        assert result == [20]

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_relevant_rows_complex(self, mock_columns):
        """Test get_relevant_rows with complex condition."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'and',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc1'}
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc2'}
                },
                {
                    'type': 'or',
                    'conditions': [
                        {
                            'type': 'simple',
                            'procedure': {'id': 'proc3'}
                        }
                    ]
                }
            ]
        }
        id_to_row = {'proc1': 25, 'proc2': 10, 'proc3': 15}
        
        result = formatter.get_relevant_rows(condition, id_to_row)
        
        # Should be sorted
        assert result == [10, 15, 25]

    @patch('yaml2sheet.condition_formatter.COLUMNS')
    def test_get_relevant_rows_nested_complex(self, mock_columns):
        """Test get_relevant_rows with deeply nested conditions."""
        mock_columns.__getitem__.side_effect = self.mock_columns.__getitem__
        mock_columns.__contains__.side_effect = self.mock_columns.__contains__
        
        formatter = ConditionFormatter(
            self.check_results, 
            self.final_results, 
            self.target_id
        )
        
        condition = {
            'type': 'or',
            'conditions': [
                {
                    'type': 'and',
                    'conditions': [
                        {
                            'type': 'simple',
                            'procedure': {'id': 'proc1'}
                        },
                        {
                            'type': 'simple',
                            'procedure': {'id': 'proc2'}
                        }
                    ]
                },
                {
                    'type': 'simple',
                    'procedure': {'id': 'proc3'}
                }
            ]
        }
        id_to_row = {'proc1': 30, 'proc2': 5, 'proc3': 20}
        
        result = formatter.get_relevant_rows(condition, id_to_row)
        
        # Should be sorted and include all procedures
        assert result == [5, 20, 30]
