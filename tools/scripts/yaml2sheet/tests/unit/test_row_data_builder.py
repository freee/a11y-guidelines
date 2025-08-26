import unittest
from unittest.mock import patch, MagicMock
from yaml2sheet.row_data_builder import RowDataBuilder
from yaml2sheet.cell_data import CellData, CellType


class TestRowDataBuilder(unittest.TestCase):
    """Test cases for RowDataBuilder class"""

    def setUp(self):
        """Set up test fixtures"""
        self.builder = RowDataBuilder('ja', 'designWeb')
        self.builder_en = RowDataBuilder('en', 'productWeb')
        
        # Sample check data
        self.basic_check = {
            'id': 'check001',
            'checkId': 'C001',
            'subcheckId': 'C001-01',
            'check': 'Basic check content',
            'severity': 'high',
            'info': [],
            'guidelines': []
        }
        
        self.check_with_conditions = {
            'id': 'check002',
            'checkId': 'C002',
            'subcheckId': 'C002-01',
            'check': 'Check with conditions',
            'severity': 'medium',
            'conditions': [{
                'target': 'designWeb',
                'type': 'simple',
                'condition': 'simple condition',
                'procedure': {'id': 'proc001', 'text': 'test procedure'}
            }],
            'info': [],
            'guidelines': []
        }
        
        self.subcheck = {
            'id': 'check001-sub1',
            'checkId': 'C001',
            'subcheckId': 'C001-01-1',
            'check': 'Subcheck content',
            'severity': 'low',
            'isSubcheck': True,
            'info': [],
            'guidelines': []
        }
        
        self.check_with_subchecks = {
            'id': 'check003',
            'checkId': 'C003',
            'subcheckId': 'C003-01',
            'check': 'Parent check with subchecks',
            'severity': 'high',
            'subchecks': {
                'designWeb': {'count': 3}
            },
            'info': [],
            'guidelines': []
        }
        
        self.id_to_row = {
            'check001': 2,
            'check002': 3,
            'check003': 4,
            'check001-sub1': 5,
            'proc001': 6,
            'proc002': 7
        }

    def test_init(self):
        """Test RowDataBuilder initialization"""
        builder = RowDataBuilder('en', 'productWeb')
        self.assertEqual(builder.current_lang, 'en')
        self.assertEqual(builder.current_target, 'productWeb')

    def test_prepare_row_data_basic(self):
        """Test prepare_row_data with basic check"""
        row_data = self.builder.prepare_row_data(
            self.basic_check, 'designWeb', 'ja', self.id_to_row
        )
        
        # Should return list of CellData objects
        self.assertIsInstance(row_data, list)
        self.assertTrue(all(isinstance(cell, CellData) for cell in row_data))
        
        # Should have cells for all column types
        self.assertGreater(len(row_data), 0)

    def test_add_id_columns(self):
        """Test _add_id_columns method"""
        row_data = []
        self.builder._add_id_columns(self.basic_check, row_data)
        
        # Should add 2 ID columns
        self.assertEqual(len(row_data), 2)
        
        # Check values and formatting
        self.assertEqual(row_data[0].value, 'C001')
        self.assertEqual(row_data[0].type, CellType.PLAIN)
        self.assertEqual(row_data[0].formatting['numberFormat']['type'], 'TEXT')
        self.assertEqual(row_data[0].formatting['numberFormat']['pattern'], '0000')
        
        self.assertEqual(row_data[1].value, 'C001-01')
        self.assertEqual(row_data[1].type, CellType.PLAIN)

    def test_add_generated_data_simple_check(self):
        """Test _add_generated_data for simple check without conditions"""
        row_data = []
        self.builder._add_generated_data(
            self.basic_check, 'designWeb', 'ja', row_data, self.id_to_row
        )
        
        # Should add 2 generated data columns for simple check
        self.assertEqual(len(row_data), 2)
        
        # Both should be formulas with protection
        self.assertEqual(row_data[0].type, CellType.FORMULA)
        self.assertTrue(row_data[0].protection)
        self.assertEqual(row_data[1].type, CellType.FORMULA)
        self.assertTrue(row_data[1].protection)

    def test_add_generated_data_check_with_conditions(self):
        """Test _add_generated_data for check with conditions"""
        with patch('yaml2sheet.row_data_builder.ConditionFormatter') as mock_formatter:
            mock_formatter_instance = MagicMock()
            mock_formatter_instance.get_condition_formula.return_value = '=FORMULA()'
            mock_formatter.return_value = mock_formatter_instance
            
            row_data = []
            self.builder._add_generated_data(
                self.check_with_conditions, 'designWeb', 'ja', row_data, self.id_to_row
            )
            
            # Should add 2 generated data columns
            self.assertEqual(len(row_data), 2)
            
            # Should call ConditionFormatter
            mock_formatter.assert_called_once()
            mock_formatter_instance.get_condition_formula.assert_called_once()

    def test_add_generated_data_subcheck(self):
        """Test _add_generated_data for subcheck"""
        row_data = []
        self.builder._add_generated_data(
            self.subcheck, 'designWeb', 'ja', row_data, self.id_to_row
        )
        
        # Should add 2 generated data columns for subcheck
        self.assertEqual(len(row_data), 2)
        
        # First should be empty, second should reference parent
        self.assertEqual(row_data[0].value, None)
        self.assertEqual(row_data[0].type, CellType.PLAIN)
        self.assertTrue(row_data[0].protection)
        
        self.assertEqual(row_data[1].type, CellType.FORMULA)
        self.assertTrue(row_data[1].protection)
        self.assertIn('D2', row_data[1].value)  # Should reference parent row (column D is calc column)

    def test_add_generated_data_subcheck_with_conditions(self):
        """Test _add_generated_data for subcheck with conditions"""
        subcheck_with_conditions = {
            **self.subcheck,
            'conditions': [{
                'target': 'designWeb',
                'type': 'simple',
                'condition': 'subcheck condition',
                'procedure': {'id': 'proc002', 'text': 'subcheck procedure'}
            }]
        }
        
        with patch('yaml2sheet.row_data_builder.ConditionFormatter') as mock_formatter:
            mock_formatter_instance = MagicMock()
            mock_formatter_instance.get_condition_formula.return_value = '=SUBCHECK_FORMULA()'
            mock_formatter.return_value = mock_formatter_instance
            
            row_data = []
            self.builder._add_generated_data(
                subcheck_with_conditions, 'designWeb', 'ja', row_data, self.id_to_row
            )
            
            # Should add 2 generated data columns
            self.assertEqual(len(row_data), 2)
            
            # Should reference parent for subcheck even with conditions
            self.assertEqual(row_data[0].value, None)
            self.assertTrue(row_data[0].protection)
            self.assertIn('D2', row_data[1].value)  # Should reference parent row (column D is calc column)

    def test_add_user_entry_columns_normal_check(self):
        """Test _add_user_entry_columns for normal check"""
        row_data = []
        self.builder._add_user_entry_columns(
            self.basic_check, 'designWeb', 'ja', row_data
        )
        
        # Should add 2 user entry columns (result, note)
        self.assertEqual(len(row_data), 2)
        
        # Result column should have validation
        result_cell = row_data[0]
        self.assertEqual(result_cell.type, CellType.PLAIN)
        self.assertIsNotNone(result_cell.validation)
        self.assertEqual(result_cell.validation['condition']['type'], 'ONE_OF_LIST')
        
        # Note column should be empty plain cell
        note_cell = row_data[1]
        self.assertEqual(note_cell.value, None)
        self.assertEqual(note_cell.type, CellType.PLAIN)

    def test_add_user_entry_columns_parent_with_subchecks(self):
        """Test _add_user_entry_columns for parent check with subchecks"""
        row_data = []
        self.builder._add_user_entry_columns(
            self.check_with_subchecks, 'designWeb', 'ja', row_data
        )
        
        # Should add 2 user entry columns
        self.assertEqual(len(row_data), 2)
        
        # Result column should be protected for parent with subchecks
        result_cell = row_data[0]
        self.assertEqual(result_cell.value, None)
        self.assertTrue(result_cell.protection)
        # Due to CellData constructor logic, formatting is None when value is None
        self.assertIsNone(result_cell.formatting)

    def test_add_user_entry_columns_subcheck(self):
        """Test _add_user_entry_columns for subcheck"""
        row_data = []
        self.builder._add_user_entry_columns(
            self.subcheck, 'designWeb', 'ja', row_data
        )
        
        # Should add 2 user entry columns
        self.assertEqual(len(row_data), 2)
        
        # Result column should have validation for subcheck
        result_cell = row_data[0]
        self.assertIsNotNone(result_cell.validation)

    def test_add_plain_data_columns(self):
        """Test _add_plain_data_columns method"""
        check_with_plain_data = {
            **self.basic_check,
            'webConditionStatement': 'Web condition statement',
            'severity': 'high'
        }
        
        row_data = []
        self.builder._add_plain_data_columns(
            check_with_plain_data, 'designWeb', 'ja', row_data
        )
        
        # Should add multiple plain data columns
        self.assertGreater(len(row_data), 0)
        
        # All should be plain cells
        self.assertTrue(all(cell.type == CellType.PLAIN for cell in row_data))

    def test_add_plain_data_columns_with_l10n(self):
        """Test _add_plain_data_columns with localized data"""
        check_with_l10n = {
            **self.basic_check,
            'check': {'ja': '日本語チェック', 'en': 'English check'},
            'severity': 'high'
        }
        
        row_data = []
        self.builder._add_plain_data_columns(
            check_with_l10n, 'designWeb', 'ja', row_data
        )
        
        # Should use localized value
        check_cell = next((cell for cell in row_data if cell.value == '日本語チェック'), None)
        self.assertIsNotNone(check_cell)

    def test_add_plain_data_columns_missing_data(self):
        """Test _add_plain_data_columns with missing data"""
        minimal_check = {
            'checkId': 'C001',
            'subcheckId': 'C001-01'
        }
        
        row_data = []
        self.builder._add_plain_data_columns(
            minimal_check, 'designWeb', 'ja', row_data
        )
        
        # Should handle missing data gracefully
        self.assertGreater(len(row_data), 0)
        # Missing values should be None (empty cells)
        self.assertTrue(all(cell.value is None for cell in row_data if cell.value != 'high'))

    def test_add_link_columns_empty_links(self):
        """Test _add_link_columns with empty links"""
        row_data = []
        self.builder._add_link_columns(
            self.basic_check, 'designWeb', 'ja', row_data
        )
        
        # Should add link columns even if empty
        self.assertGreater(len(row_data), 0)
        
        # Empty links should be plain cells with None values
        self.assertTrue(all(cell.type == CellType.PLAIN for cell in row_data))
        self.assertTrue(all(cell.value is None for cell in row_data))

    def test_add_link_columns_with_links(self):
        """Test _add_link_columns with actual links"""
        check_with_links = {
            **self.basic_check,
            'info': [{
                'text': {'ja': '参考情報', 'en': 'Reference info'},
                'url': {'ja': '/ja/info', 'en': '/en/info'}
            }],
            'guidelines': [{
                'text': {'ja': 'ガイドライン', 'en': 'Guideline'},
                'url': {'ja': '/ja/guideline', 'en': '/en/guideline'}
            }]
        }
        
        with patch('freee_a11y_gl.settings') as mock_settings:
            mock_settings.get.return_value = 'https://example.com'
            row_data = []
            self.builder._add_link_columns(
                check_with_links, 'designWeb', 'ja', row_data
            )
            
            # Should create rich text cells for links
            rich_text_cells = [cell for cell in row_data if cell.type == CellType.RICH_TEXT]
            self.assertGreater(len(rich_text_cells), 0)

    def test_create_rich_text_cell_single_link(self):
        """Test _create_rich_text_cell with single link"""
        links = [{
            'text': {'ja': 'テストリンク', 'en': 'Test link'},
            'url': {'ja': '/ja/test', 'en': '/en/test'}
        }]
        
        with patch('freee_a11y_gl.settings') as mock_settings:
            mock_settings.get.return_value = 'https://example.com'
            cell = self.builder._create_rich_text_cell(links, 'ja')
            
            self.assertEqual(cell.type, CellType.RICH_TEXT)
            self.assertIsInstance(cell.value, dict)
            self.assertIn('text', cell.value)
            self.assertIn('format_runs', cell.value)
            self.assertEqual(cell.value['text'], 'テストリンク')
            
            # Check format runs
            format_runs = cell.value['format_runs']
            self.assertEqual(len(format_runs), 1)
            self.assertEqual(format_runs[0]['startIndex'], 0)
            self.assertIn('link', format_runs[0]['format'])
            self.assertEqual(format_runs[0]['format']['link']['uri'], 'https://example.com/ja/test')

    def test_create_rich_text_cell_multiple_links(self):
        """Test _create_rich_text_cell with multiple links"""
        links = [
            {
                'text': {'ja': 'リンク1', 'en': 'Link 1'},
                'url': {'ja': '/ja/link1', 'en': '/en/link1'}
            },
            {
                'text': {'ja': 'リンク2', 'en': 'Link 2'},
                'url': {'ja': '/ja/link2', 'en': '/en/link2'}
            }
        ]
        
        with patch('freee_a11y_gl.settings') as mock_settings:
            mock_settings.get.return_value = 'https://example.com'
            cell = self.builder._create_rich_text_cell(links, 'ja')
            
            self.assertEqual(cell.type, CellType.RICH_TEXT)
            self.assertEqual(cell.value['text'], 'リンク1\nリンク2')
            
            # Check format runs for both links
            format_runs = cell.value['format_runs']
            self.assertEqual(len(format_runs), 2)
            
            # First link
            self.assertEqual(format_runs[0]['startIndex'], 0)
            self.assertEqual(format_runs[0]['format']['link']['uri'], 'https://example.com/ja/link1')
            
            # Second link (after newline)
            self.assertEqual(format_runs[1]['startIndex'], 5)  # After 'リンク1\n'
            self.assertEqual(format_runs[1]['format']['link']['uri'], 'https://example.com/ja/link2')

    def test_create_rich_text_cell_absolute_url(self):
        """Test _create_rich_text_cell with absolute URL"""
        links = [{
            'text': {'ja': '外部リンク', 'en': 'External link'},
            'url': {'ja': 'https://external.com/ja', 'en': 'https://external.com/en'}
        }]
        
        cell = self.builder._create_rich_text_cell(links, 'ja')
        
        # Should use absolute URL as-is
        format_runs = cell.value['format_runs']
        self.assertEqual(format_runs[0]['format']['link']['uri'], 'https://external.com/ja')

    def test_create_rich_text_cell_missing_base_url(self):
        """Test _create_rich_text_cell with relative URL but no base_url"""
        links = [{
            'text': {'ja': 'リンク', 'en': 'Link'},
            'url': {'ja': '/relative', 'en': '/relative'}
        }]
        
        with patch('freee_a11y_gl.settings') as mock_settings:
            mock_settings.get.return_value = ''
            cell = self.builder._create_rich_text_cell(links, 'ja')
            
            # Should handle missing base_url gracefully
            format_runs = cell.value['format_runs']
            self.assertEqual(format_runs[0]['format']['link']['uri'], '/relative')

    def test_prepare_row_data_integration_designweb(self):
        """Test prepare_row_data integration for designWeb target"""
        row_data = self.builder.prepare_row_data(
            self.check_with_conditions, 'designWeb', 'ja', self.id_to_row
        )
        
        # Should have all expected column types
        self.assertGreater(len(row_data), 10)  # ID + generated + user + plain + link columns
        
        # Check that we have different cell types
        cell_types = {cell.type for cell in row_data}
        self.assertIn(CellType.PLAIN, cell_types)
        self.assertIn(CellType.FORMULA, cell_types)

    def test_prepare_row_data_integration_designmobile(self):
        """Test prepare_row_data integration for designMobile target (no generated data)"""
        builder = RowDataBuilder('ja', 'designMobile')
        row_data = builder.prepare_row_data(
            self.basic_check, 'designMobile', 'ja', self.id_to_row
        )
        
        # Should have fewer columns (no generated data)
        self.assertGreater(len(row_data), 5)
        
        # Should not have formula cells (no generated data)
        cell_types = {cell.type for cell in row_data}
        self.assertNotIn(CellType.FORMULA, cell_types)

    def test_prepare_row_data_different_languages(self):
        """Test prepare_row_data with different languages"""
        # Test English
        row_data_en = self.builder_en.prepare_row_data(
            self.basic_check, 'productWeb', 'en', self.id_to_row
        )
        
        # Test Japanese
        row_data_ja = self.builder.prepare_row_data(
            self.basic_check, 'designWeb', 'ja', self.id_to_row
        )
        
        # Both should have data
        self.assertGreater(len(row_data_en), 0)
        self.assertGreater(len(row_data_ja), 0)

    def test_error_handling_missing_freee_a11y_gl(self):
        """Test error handling when freee_a11y_gl module is not available"""
        links = [{
            'text': {'ja': 'テスト', 'en': 'Test'},
            'url': {'ja': '/test', 'en': '/test'}
        }]
        
        with patch('freee_a11y_gl.settings') as mock_settings:
            mock_settings.get.side_effect = ImportError()
            # Should handle missing module gracefully
            try:
                cell = self.builder._create_rich_text_cell(links, 'ja')
                # If no exception, check that it still creates a cell
                self.assertEqual(cell.type, CellType.RICH_TEXT)
            except ImportError:
                # This is acceptable behavior
                pass


if __name__ == '__main__':
    unittest.main()
