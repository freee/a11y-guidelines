import unittest
from unittest.mock import patch, MagicMock
from yaml2sheet.column_manager import ColumnManager


class TestColumnManager(unittest.TestCase):
    """Test cases for ColumnManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.design_web_manager = ColumnManager('designWeb')
        self.design_mobile_manager = ColumnManager('designMobile')
        self.product_web_manager = ColumnManager('productWeb')
        self.code_web_manager = ColumnManager('codeWeb')

    def test_init(self):
        """Test ColumnManager initialization"""
        manager = ColumnManager('designWeb')
        self.assertEqual(manager.target_id, 'designWeb')

    def test_get_header_ids_design_web(self):
        """Test get_header_ids for designWeb target"""
        headers = self.design_web_manager.get_header_ids()
        
        # Should include all column types in correct order
        expected_start = ['checkId', 'subcheckId', 'finalResult', 'calculatedResult', 'result', 'note']
        self.assertEqual(headers[:6], expected_start)
        
        # Should include common plain data
        self.assertIn('check', headers)
        self.assertIn('severity', headers)
        
        # Should include design web specific data
        self.assertIn('webConditionStatement', headers)
        
        # Should include common link data
        self.assertIn('info', headers)
        self.assertIn('guidelines', headers)

    def test_get_header_ids_design_mobile(self):
        """Test get_header_ids for designMobile target"""
        headers = self.design_mobile_manager.get_header_ids()
        
        # Should include ID columns and user entered columns
        expected_start = ['checkId', 'subcheckId', 'result', 'note']
        self.assertEqual(headers[:4], expected_start)
        
        # Should not include generated data columns for designMobile
        self.assertNotIn('finalResult', headers)
        self.assertNotIn('calculatedResult', headers)

    def test_get_header_ids_product_web(self):
        """Test get_header_ids for productWeb target"""
        headers = self.product_web_manager.get_header_ids()
        
        # Should include generated data columns
        self.assertIn('finalResult', headers)
        self.assertIn('calculatedResult', headers)
        
        # Should include product web specific data
        self.assertIn('webConditionStatement', headers)
        self.assertIn('webTools', headers)

    def test_get_header_ids_code_web(self):
        """Test get_header_ids for codeWeb target"""
        headers = self.code_web_manager.get_header_ids()
        
        # Should include code web specific data
        self.assertIn('implementation_web', headers)
        
        # Should not include generated data columns for codeWeb
        self.assertNotIn('finalResult', headers)
        self.assertNotIn('calculatedResult', headers)

    def test_get_header_names_japanese(self):
        """Test get_header_names with Japanese language"""
        names = self.design_web_manager.get_header_names('ja')
        
        # Check some specific Japanese translations
        self.assertIn('ID', names)
        self.assertIn('最終結果', names)
        self.assertIn('判定結果（自動）', names)
        self.assertIn('チェック結果を記入', names)
        self.assertIn('チェック内容', names)

    def test_get_header_names_english(self):
        """Test get_header_names with English language"""
        names = self.design_web_manager.get_header_names('en')
        
        # Check some specific English translations
        self.assertIn('ID', names)
        self.assertIn('Final Result', names)
        self.assertIn('Final Result (Auto)', names)
        self.assertIn('Fill in the Check Result', names)
        self.assertIn('Check Details', names)

    def test_get_header_names_missing_translation(self):
        """Test get_header_names with missing translation falls back to header ID"""
        # Mock a header that doesn't exist in COLUMN_INFO
        with patch('yaml2sheet.column_manager.COLUMN_INFO', {
            'name': {
                'checkId': {'ja': 'ID', 'en': 'ID'},
                # Missing other headers
            }
        }):
            manager = ColumnManager('designWeb')
            names = manager.get_header_names('ja')
            
            # Should fall back to header ID for missing translations
            self.assertIn('finalResult', names)  # Falls back to header ID

    def test_get_column_widths(self):
        """Test get_column_widths returns correct widths"""
        widths = self.design_web_manager.get_column_widths()
        
        # Should return list of integers
        self.assertIsInstance(widths, list)
        self.assertTrue(all(isinstance(w, int) for w in widths))
        
        # Should have same length as headers
        headers = self.design_web_manager.get_header_ids()
        self.assertEqual(len(widths), len(headers))
        
        # Check some specific widths
        headers = self.design_web_manager.get_header_ids()
        checkId_index = headers.index('checkId')
        self.assertEqual(widths[checkId_index], 43)

    def test_get_column_widths_missing_width(self):
        """Test get_column_widths with missing width falls back to default"""
        # Mock COLUMN_INFO with missing width
        with patch('yaml2sheet.column_manager.COLUMN_INFO', {
            'width': {
                'checkId': 43,
                # Missing other widths
            }
        }):
            manager = ColumnManager('designWeb')
            widths = manager.get_column_widths()
            
            # Should use default width (100) for missing entries
            self.assertIn(100, widths)

    def test_has_generated_data_true(self):
        """Test has_generated_data returns True for targets with generated data"""
        self.assertTrue(self.design_web_manager.has_generated_data())
        self.assertTrue(self.product_web_manager.has_generated_data())

    def test_has_generated_data_false(self):
        """Test has_generated_data returns False for targets without generated data"""
        self.assertFalse(self.design_mobile_manager.has_generated_data())
        self.assertFalse(self.code_web_manager.has_generated_data())

    def test_get_generated_data_column_count_with_data(self):
        """Test get_generated_data_column_count for targets with generated data"""
        count = self.design_web_manager.get_generated_data_column_count()
        self.assertEqual(count, 2)  # finalResult, calculatedResult
        
        count = self.product_web_manager.get_generated_data_column_count()
        self.assertEqual(count, 2)  # finalResult, calculatedResult

    def test_get_generated_data_column_count_without_data(self):
        """Test get_generated_data_column_count for targets without generated data"""
        count = self.design_mobile_manager.get_generated_data_column_count()
        self.assertEqual(count, 0)
        
        count = self.code_web_manager.get_generated_data_column_count()
        self.assertEqual(count, 0)

    def test_get_result_column_index_with_generated_data(self):
        """Test get_result_column_index for targets with generated data"""
        index = self.design_web_manager.get_result_column_index()
        # ID columns (2) + generated data columns (2) = 4
        self.assertEqual(index, 4)

    def test_get_result_column_index_without_generated_data(self):
        """Test get_result_column_index for targets without generated data"""
        index = self.design_mobile_manager.get_result_column_index()
        # ID columns (2) + generated data columns (0) = 2
        self.assertEqual(index, 2)

    def test_different_target_configurations(self):
        """Test various target configurations"""
        # Test productIos
        ios_manager = ColumnManager('productIos')
        headers = ios_manager.get_header_ids()
        self.assertIn('iosConditionStatement', headers)
        self.assertIn('iosTools', headers)
        self.assertTrue(ios_manager.has_generated_data())

        # Test productAndroid
        android_manager = ColumnManager('productAndroid')
        headers = android_manager.get_header_ids()
        self.assertIn('androidConditionStatement', headers)
        self.assertIn('androidTools', headers)
        self.assertTrue(android_manager.has_generated_data())

        # Test codeMobile
        code_mobile_manager = ColumnManager('codeMobile')
        headers = code_mobile_manager.get_header_ids()
        self.assertIn('implementation_ios', headers)
        self.assertIn('implementation_android', headers)
        self.assertFalse(code_mobile_manager.has_generated_data())

    def test_header_order_consistency(self):
        """Test that header order is consistent across calls"""
        headers1 = self.design_web_manager.get_header_ids()
        headers2 = self.design_web_manager.get_header_ids()
        self.assertEqual(headers1, headers2)

        names1 = self.design_web_manager.get_header_names('ja')
        names2 = self.design_web_manager.get_header_names('ja')
        self.assertEqual(names1, names2)

        widths1 = self.design_web_manager.get_column_widths()
        widths2 = self.design_web_manager.get_column_widths()
        self.assertEqual(widths1, widths2)


if __name__ == '__main__':
    unittest.main()
