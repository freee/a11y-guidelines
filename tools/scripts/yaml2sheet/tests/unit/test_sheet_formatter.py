"""
Tests for sheet_formatter module.

Tests the SheetFormatter class which handles sheet formatting operations including:
- Basic sheet formatting (headers, cell wrapping, frozen rows)
- Conditional formatting for pass/fail results
- Sheet protection settings
- Parent check cell protection
"""

import pytest
from unittest.mock import Mock, patch
from yaml2sheet.sheet_formatter import SheetFormatter
from yaml2sheet.sheet_structure import SheetStructure
from yaml2sheet.cell_data import CellData, CellType
from yaml2sheet.config import CHECK_RESULTS, FINAL_CHECK_RESULTS, COLUMNS


class TestSheetFormatter:
    """Test SheetFormatter functionality."""
    
    def test_init_basic(self):
        """Test basic initialization."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        assert formatter.current_lang == 'ja'
        assert formatter.current_target == 'designWeb'
        assert formatter.editor_email == 'test@example.com'
    
    def test_init_no_editor_email(self):
        """Test initialization without editor email."""
        formatter = SheetFormatter('en', 'productWeb')
        assert formatter.current_lang == 'en'
        assert formatter.current_target == 'productWeb'
        assert formatter.editor_email == ""
    
    def test_apply_basic_formatting(self):
        """Test basic sheet formatting application."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        data_length = 10
        
        requests = formatter.apply_basic_formatting(sheet_id, data_length)
        
        assert len(requests) == 3
        
        # Check header formatting request
        header_request = requests[0]
        assert header_request['repeatCell']['range']['sheetId'] == sheet_id
        assert header_request['repeatCell']['range']['startRowIndex'] == 0
        assert header_request['repeatCell']['range']['endRowIndex'] == 1
        assert header_request['repeatCell']['cell']['userEnteredFormat']['backgroundColor'] == {
            'red': 0.9, 'green': 0.9, 'blue': 0.9
        }
        assert header_request['repeatCell']['cell']['userEnteredFormat']['textFormat']['bold'] is True
        assert header_request['repeatCell']['cell']['userEnteredFormat']['verticalAlignment'] == 'MIDDLE'
        assert header_request['repeatCell']['cell']['userEnteredFormat']['wrapStrategy'] == 'WRAP'
        
        # Check data cell wrap strategy request
        wrap_request = requests[1]
        assert wrap_request['repeatCell']['range']['sheetId'] == sheet_id
        assert wrap_request['repeatCell']['range']['startRowIndex'] == 1
        assert wrap_request['repeatCell']['range']['endRowIndex'] == data_length + 1
        assert wrap_request['repeatCell']['cell']['userEnteredFormat']['wrapStrategy'] == 'WRAP'
        
        # Check freeze row request
        freeze_request = requests[2]
        assert freeze_request['updateSheetProperties']['properties']['sheetId'] == sheet_id
        assert freeze_request['updateSheetProperties']['properties']['gridProperties']['frozenRowCount'] == 1
    
    def test_get_result_column_index_with_generated_data(self):
        """Test getting result column index for target with generated data."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        
        # designWeb has generated data, so result column should be after id columns + generated data
        expected_index = len(COLUMNS['idCols']) + len(COLUMNS['designWeb']['generatedData'])
        assert formatter.get_result_column_index() == expected_index
    
    def test_get_result_column_index_without_generated_data(self):
        """Test getting result column index for target without generated data."""
        formatter = SheetFormatter('ja', 'designMobile', 'test@example.com')
        
        # designMobile has no generated data, so result column should be after id columns only
        expected_index = len(COLUMNS['idCols']) + len(COLUMNS['designMobile']['generatedData'])
        assert formatter.get_result_column_index() == expected_index
    
    def test_add_conditional_formatting_with_generated_data(self):
        """Test conditional formatting for target with generated data."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        data_length = 10
        
        requests = formatter.add_conditional_formatting(sheet_id, data_length)
        
        # Should have 4 requests: 2 for user-entered results + 2 for generated results
        assert len(requests) == 4
        
        # Check user-entered pass condition
        user_pass_request = requests[0]
        result_column = formatter.get_result_column_index()
        assert user_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['sheetId'] == sheet_id
        assert user_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['startRowIndex'] == 1
        assert user_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['endRowIndex'] == data_length + 1
        assert user_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['startColumnIndex'] == result_column
        assert user_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['endColumnIndex'] == result_column + 1
        assert user_pass_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['type'] == 'TEXT_EQ'
        assert user_pass_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['pass']['ja']
        assert user_pass_request['addConditionalFormatRule']['rule']['booleanRule']['format']['backgroundColor'] == {
            'red': 0.85, 'green': 0.92, 'blue': 0.83
        }
        
        # Check user-entered fail condition
        user_fail_request = requests[1]
        assert user_fail_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['fail']['ja']
        assert user_fail_request['addConditionalFormatRule']['rule']['booleanRule']['format']['backgroundColor'] == {
            'red': 0.96, 'green': 0.80, 'blue': 0.80
        }
        
        # Check generated pass condition
        generated_pass_request = requests[2]
        generated_column_start = len(COLUMNS['idCols']) + 1
        generated_column_end = len(COLUMNS['idCols']) + len(COLUMNS['designWeb']['generatedData'])
        assert generated_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['startColumnIndex'] == generated_column_start
        assert generated_pass_request['addConditionalFormatRule']['rule']['ranges'][0]['endColumnIndex'] == generated_column_end
        assert generated_pass_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == FINAL_CHECK_RESULTS['pass']['ja']
        
        # Check generated fail condition
        generated_fail_request = requests[3]
        assert generated_fail_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == FINAL_CHECK_RESULTS['fail']['ja']
    
    def test_add_conditional_formatting_without_generated_data(self):
        """Test conditional formatting for target without generated data."""
        formatter = SheetFormatter('ja', 'designMobile', 'test@example.com')
        sheet_id = 123
        data_length = 10
        
        requests = formatter.add_conditional_formatting(sheet_id, data_length)
        
        # Should have only 2 requests for user-entered results (no generated data)
        assert len(requests) == 2
        
        # Check that only user-entered conditions are present
        assert all('TEXT_EQ' in req['addConditionalFormatRule']['rule']['booleanRule']['condition']['type'] for req in requests)
        assert requests[0]['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['pass']['ja']
        assert requests[1]['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['fail']['ja']
    
    def test_add_conditional_formatting_english(self):
        """Test conditional formatting with English language."""
        formatter = SheetFormatter('en', 'productWeb', 'test@example.com')
        sheet_id = 123
        data_length = 5
        
        requests = formatter.add_conditional_formatting(sheet_id, data_length)
        
        # Check that English values are used
        user_pass_request = requests[0]
        assert user_pass_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['pass']['en']
        
        user_fail_request = requests[1]
        assert user_fail_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == CHECK_RESULTS['fail']['en']
        
        # Check generated data conditions use English
        generated_pass_request = requests[2]
        assert generated_pass_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == FINAL_CHECK_RESULTS['pass']['en']
        
        generated_fail_request = requests[3]
        assert generated_fail_request['addConditionalFormatRule']['rule']['booleanRule']['condition']['values'][0]['userEnteredValue'] == FINAL_CHECK_RESULTS['fail']['en']
    
    def test_add_protection_settings_with_generated_data(self):
        """Test protection settings for target with generated data."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        
        # Create mock sheet structure
        sheet = Mock(spec=SheetStructure)
        sheet.data = [
            [CellData('Header1', CellType.PLAIN), CellData('Header2', CellType.PLAIN)],
            [CellData('Data1', CellType.PLAIN), CellData('Data2', CellType.PLAIN)],
            [CellData('Data3', CellType.PLAIN), CellData('Data4', CellType.PLAIN)]
        ]
        
        requests = formatter.add_protection_settings(sheet_id, sheet)
        
        assert len(requests) == 1
        
        protection_request = requests[0]
        assert protection_request['addProtectedRange']['protectedRange']['range']['sheetId'] == sheet_id
        assert protection_request['addProtectedRange']['protectedRange']['range']['startRowIndex'] == 1
        assert protection_request['addProtectedRange']['protectedRange']['range']['endRowIndex'] == len(sheet.data) + 1
        
        generated_data_start = len(COLUMNS['idCols'])
        generated_data_count = len(COLUMNS['designWeb']['generatedData'])
        assert protection_request['addProtectedRange']['protectedRange']['range']['startColumnIndex'] == generated_data_start
        assert protection_request['addProtectedRange']['protectedRange']['range']['endColumnIndex'] == generated_data_start + generated_data_count
        
        assert protection_request['addProtectedRange']['protectedRange']['description'] == 'Generated data protection'
        assert protection_request['addProtectedRange']['protectedRange']['warningOnly'] is False
        assert protection_request['addProtectedRange']['protectedRange']['editors']['domainUsersCanEdit'] is False
        assert protection_request['addProtectedRange']['protectedRange']['editors']['users'] == ['test@example.com']
    
    def test_add_protection_settings_without_generated_data(self):
        """Test protection settings for target without generated data."""
        formatter = SheetFormatter('ja', 'designMobile', 'test@example.com')
        sheet_id = 123
        
        # Create mock sheet structure
        sheet = Mock(spec=SheetStructure)
        sheet.data = [
            [CellData('Header1', CellType.PLAIN), CellData('Header2', CellType.PLAIN)],
            [CellData('Data1', CellType.PLAIN), CellData('Data2', CellType.PLAIN)]
        ]
        
        requests = formatter.add_protection_settings(sheet_id, sheet)
        
        # Should have no protection requests for targets without generated data
        assert len(requests) == 0
    
    def test_add_protection_settings_no_editor_email(self):
        """Test protection settings without editor email."""
        formatter = SheetFormatter('ja', 'designWeb', '')
        sheet_id = 123
        
        # Create mock sheet structure
        sheet = Mock(spec=SheetStructure)
        sheet.data = [
            [CellData('Header1', CellType.PLAIN), CellData('Header2', CellType.PLAIN)],
            [CellData('Data1', CellType.PLAIN), CellData('Data2', CellType.PLAIN)]
        ]
        
        requests = formatter.add_protection_settings(sheet_id, sheet)
        
        assert len(requests) == 1
        protection_request = requests[0]
        
        # Should not have users field when no editor email
        assert 'users' not in protection_request['addProtectedRange']['protectedRange']['editors']
        assert protection_request['addProtectedRange']['protectedRange']['editors']['domainUsersCanEdit'] is False
    
    def test_protect_parent_check_cells(self):
        """Test protection of parent check cells."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        row_index = 5
        
        request = formatter.protect_parent_check_cells(sheet_id, row_index)
        
        result_column = formatter.get_result_column_index()
        assert request['addProtectedRange']['protectedRange']['range']['sheetId'] == sheet_id
        assert request['addProtectedRange']['protectedRange']['range']['startRowIndex'] == row_index
        assert request['addProtectedRange']['protectedRange']['range']['endRowIndex'] == row_index + 1
        assert request['addProtectedRange']['protectedRange']['range']['startColumnIndex'] == result_column
        assert request['addProtectedRange']['protectedRange']['range']['endColumnIndex'] == result_column + 1
        assert request['addProtectedRange']['protectedRange']['description'] == 'Parent check cell protection'
        assert request['addProtectedRange']['protectedRange']['warningOnly'] is False
        assert request['addProtectedRange']['protectedRange']['editors']['domainUsersCanEdit'] is False
        assert request['addProtectedRange']['protectedRange']['editors']['users'] == ['test@example.com']
    
    def test_protect_parent_check_cells_no_editor_email(self):
        """Test protection of parent check cells without editor email."""
        formatter = SheetFormatter('ja', 'designWeb', '')
        sheet_id = 123
        row_index = 3
        
        request = formatter.protect_parent_check_cells(sheet_id, row_index)
        
        # Should not have users field when no editor email
        assert 'users' not in request['addProtectedRange']['protectedRange']['editors']
        assert request['addProtectedRange']['protectedRange']['editors']['domainUsersCanEdit'] is False
    
    def test_different_targets_column_calculations(self):
        """Test column calculations for different targets."""
        targets_with_generated = ['designWeb', 'productWeb', 'productIos', 'productAndroid']
        targets_without_generated = ['designMobile', 'codeWeb', 'codeMobile']
        
        for target in targets_with_generated:
            formatter = SheetFormatter('ja', target, 'test@example.com')
            expected_index = len(COLUMNS['idCols']) + len(COLUMNS[target]['generatedData'])
            assert formatter.get_result_column_index() == expected_index
        
        for target in targets_without_generated:
            formatter = SheetFormatter('ja', target, 'test@example.com')
            expected_index = len(COLUMNS['idCols']) + len(COLUMNS[target]['generatedData'])
            assert formatter.get_result_column_index() == expected_index
    
    def test_conditional_formatting_range_calculations(self):
        """Test conditional formatting range calculations for different data lengths."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        
        # Test with different data lengths
        for data_length in [1, 5, 10, 100]:
            requests = formatter.add_conditional_formatting(sheet_id, data_length)
            
            for request in requests:
                range_info = request['addConditionalFormatRule']['rule']['ranges'][0]
                assert range_info['startRowIndex'] == 1
                assert range_info['endRowIndex'] == data_length + 1
                assert range_info['sheetId'] == sheet_id
    
    def test_protection_settings_with_different_sheet_sizes(self):
        """Test protection settings with different sheet sizes."""
        formatter = SheetFormatter('ja', 'designWeb', 'test@example.com')
        sheet_id = 123
        
        # Test with different sheet sizes
        for num_rows in [2, 5, 10, 50]:
            sheet = Mock(spec=SheetStructure)
            sheet.data = [[CellData('test', CellType.PLAIN)] * 5 for _ in range(num_rows)]
            
            requests = formatter.add_protection_settings(sheet_id, sheet)
            
            if len(COLUMNS['designWeb']['generatedData']) > 0:
                assert len(requests) == 1
                protection_request = requests[0]
                assert protection_request['addProtectedRange']['protectedRange']['range']['endRowIndex'] == num_rows + 1
    
    def test_formatting_consistency_across_languages(self):
        """Test that formatting is consistent across languages."""
        sheet_id = 123
        data_length = 10
        
        for lang in ['ja', 'en']:
            formatter = SheetFormatter(lang, 'designWeb', 'test@example.com')
            
            # Basic formatting should be identical
            basic_requests = formatter.apply_basic_formatting(sheet_id, data_length)
            assert len(basic_requests) == 3
            
            # Conditional formatting should have same structure but different values
            conditional_requests = formatter.add_conditional_formatting(sheet_id, data_length)
            assert len(conditional_requests) == 4
            
            # Protection should be identical
            sheet = Mock(spec=SheetStructure)
            sheet.data = [[CellData('test', CellType.PLAIN)] * 5 for _ in range(data_length)]
            protection_requests = formatter.add_protection_settings(sheet_id, sheet)
            assert len(protection_requests) == 1
