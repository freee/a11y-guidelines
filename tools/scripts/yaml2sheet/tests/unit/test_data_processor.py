"""
Tests for data_processor module.

Tests the DataProcessor class for processing source checklist data.
"""

import pytest
from unittest.mock import patch, MagicMock
from yaml2sheet.data_processor import DataProcessor
from yaml2sheet.sheet_structure import CheckInfo
from yaml2sheet.utils import format_statement_summary


class TestDataProcessor:
    """Test DataProcessor class functionality."""
    
    def test_init(self):
        """Test DataProcessor initialization."""
        processor = DataProcessor()
        
        assert isinstance(processor.check_info, dict)
        assert len(processor.check_info) == 0
    
    def test_process_source_data_empty(self):
        """Test processing empty source data."""
        processor = DataProcessor()
        result = processor.process_source_data({})
        
        # Should return empty data for all targets
        expected_targets = [
            'designWeb', 'designMobile', 'codeWeb', 'codeMobile',
            'productWeb', 'productIos', 'productAndroid'
        ]
        
        for target in expected_targets:
            assert target in result
            assert result[target] == []
    
    def test_process_source_data_basic_check(self):
        """Test processing basic check data."""
        processor = DataProcessor()
        
        source_data = {
            'check1': {
                'id': 'check1',
                'sortKey': 1,
                'target': 'design',
                'platform': ['web'],
                'check': {'ja': 'テストチェック', 'en': 'Test check'},
                'severity': 'high'
            }
        }
        
        result = processor.process_source_data(source_data)
        
        # Check that data was processed
        assert 'designWeb' in result
        assert len(result['designWeb']) == 1
        
        processed_check = result['designWeb'][0]
        assert processed_check['checkId'] == 'check1'
        assert processed_check['subcheckId'] == ""
        assert processed_check['sheetNames'] == ['designWeb']
        assert processed_check['isSubcheck'] is False
        assert 'subchecks' in processed_check
    
    def test_process_source_data_mobile_platform_expansion(self):
        """Test that mobile platform is expanded to ios and android."""
        processor = DataProcessor()
        
        source_data = {
            'check1': {
                'id': 'check1',
                'sortKey': 1,
                'target': 'product',
                'platform': ['mobile'],
                'check': {'ja': 'モバイルチェック', 'en': 'Mobile check'},
                'severity': 'medium'
            }
        }
        
        result = processor.process_source_data(source_data)
        
        processed_check = result['productIos'][0]
        assert 'ios' in processed_check['platform']
        assert 'android' in processed_check['platform']
        assert 'mobile' in processed_check['platform']
        
        # Should appear in both iOS and Android sheets
        assert len(result['productIos']) == 1
        assert len(result['productAndroid']) == 1
    
    def test_process_source_data_sort_by_sort_key(self):
        """Test that data is sorted by sortKey."""
        processor = DataProcessor()
        
        source_data = {
            'check3': {
                'id': 'check3',
                'sortKey': 3,
                'target': 'design',
                'platform': ['web'],
                'check': {'ja': 'チェック3', 'en': 'Check 3'},
                'severity': 'low'
            },
            'check1': {
                'id': 'check1',
                'sortKey': 1,
                'target': 'design',
                'platform': ['web'],
                'check': {'ja': 'チェック1', 'en': 'Check 1'},
                'severity': 'high'
            },
            'check2': {
                'id': 'check2',
                'sortKey': 2,
                'target': 'design',
                'platform': ['web'],
                'check': {'ja': 'チェック2', 'en': 'Check 2'},
                'severity': 'medium'
            }
        }
        
        result = processor.process_source_data(source_data)
        
        # Should be sorted by sortKey
        checks = result['designWeb']
        assert len(checks) == 3
        assert checks[0]['id'] == 'check1'
        assert checks[1]['id'] == 'check2'
        assert checks[2]['id'] == 'check3'
    
    def test_process_source_data_missing_sort_key(self):
        """Test processing data with missing sortKey."""
        processor = DataProcessor()
        
        source_data = {
            'check1': {
                'id': 'check1',
                # No sortKey
                'target': 'design',
                'platform': ['web'],
                'check': {'ja': 'チェック', 'en': 'Check'},
                'severity': 'medium'
            }
        }
        
        result = processor.process_source_data(source_data)
        
        # Should still process (sortKey defaults to 0)
        assert len(result['designWeb']) == 1
        assert result['designWeb'][0]['id'] == 'check1'

    def test_process_source_data_invalid_target_platform_combination(self):
        """Test processing data with invalid target/platform combination that doesn't exist in TARGET_NAMES."""
        processor = DataProcessor()
        
        source_data = {
            'check1': {
                'id': 'check1',
                'sortKey': 1,
                'target': 'invalid',  # This target doesn't exist in TARGET_NAMES
                'platform': ['web'],
                'check': {'ja': 'チェック', 'en': 'Check'},
                'severity': 'medium'
            }
        }
        
        result = processor.process_source_data(source_data)
        
        # Should process but not appear in any sheets since target_id doesn't exist
        processed_check = None
        for target_data in result.values():
            if target_data:
                processed_check = target_data[0]
                break
        
        # The check should be processed but sheetNames should be empty
        # since the target_id 'invalidWeb' doesn't exist in TARGET_NAMES
        if processed_check:
            assert processed_check['sheetNames'] == []
        else:
            # All target sheets should be empty
            for target_data in result.values():
                assert len(target_data) == 0
    
    def test_has_generated_data_true(self):
        """Test _has_generated_data returns True when sheets require generated data."""
        processor = DataProcessor()
        
        # productWeb has generated data according to COLUMNS config
        sheet_names = ['productWeb']
        result = processor._has_generated_data(sheet_names)
        
        assert result is True
    
    def test_has_generated_data_false(self):
        """Test _has_generated_data returns False when sheets don't require generated data."""
        processor = DataProcessor()
        
        # designMobile has no generated data according to COLUMNS config
        sheet_names = ['designMobile']
        result = processor._has_generated_data(sheet_names)
        
        assert result is False
    
    def test_has_generated_data_mixed(self):
        """Test _has_generated_data returns True when any sheet requires generated data."""
        processor = DataProcessor()
        
        # Mix of sheets with and without generated data
        sheet_names = ['designMobile', 'productWeb']
        result = processor._has_generated_data(sheet_names)
        
        assert result is True
    
    def test_has_generated_data_unknown_sheet(self):
        """Test _has_generated_data with unknown sheet name."""
        processor = DataProcessor()
        
        sheet_names = ['unknownSheet']
        result = processor._has_generated_data(sheet_names)
        
        assert result is False
    
    def test_process_standard_fields(self):
        """Test _process_standard_fields method."""
        processor = DataProcessor()
        
        check = {
            'platform': ['web', 'ios']
        }
        
        processor._process_standard_fields(check)
        
        assert check['webConditionStatement'] == ""
        assert check['iosConditionStatement'] == ""
        assert check['isSubcheck'] is False
        assert check['subchecks'] == {}
    
    def test_format_statement_summary(self):
        """Test format_statement_summary function from utils."""
        statement = {
            'ja': 'テストが動作する',
            'en': 'the test works'
        }
        
        result = format_statement_summary(statement)
        
        expected = {
            'ja': 'テストが動作することを確認する。',
            'en': 'Verify that the test works.'
        }
        assert result == expected
    
    def test_extract_procedures_simple(self):
        """Test _extract_procedures with simple condition."""
        processor = DataProcessor()
        
        condition = {
            'type': 'simple',
            'procedure': {
                'id': 'proc1',
                'platform': 'web',
                'target': 'design',
                'tool': 'manual',
                'procedure': {'ja': '手順1', 'en': 'Procedure 1'},
                'toolLink': {'text': {'ja': 'リンク', 'en': 'Link'}, 'url': {'ja': 'http://example.com', 'en': 'http://example.com'}}
            }
        }
        
        result = processor._extract_procedures(condition)
        
        assert len(result) == 1
        assert result[0]['id'] == 'proc1'
        assert result[0]['platform'] == 'web'
    
    def test_extract_procedures_complex(self):
        """Test _extract_procedures with complex nested conditions."""
        processor = DataProcessor()
        
        condition = {
            'type': 'complex',
            'conditions': [
                {
                    'type': 'simple',
                    'procedure': {
                        'id': 'proc1',
                        'platform': 'web',
                        'target': 'design',
                        'tool': 'manual',
                        'procedure': {'ja': '手順1', 'en': 'Procedure 1'},
                        'toolLink': {'text': {'ja': 'リンク1', 'en': 'Link1'}, 'url': {'ja': 'http://example1.com', 'en': 'http://example1.com'}}
                    }
                },
                {
                    'type': 'simple',
                    'procedure': {
                        'id': 'proc2',
                        'platform': 'web',
                        'target': 'design',
                        'tool': 'manual',
                        'procedure': {'ja': '手順2', 'en': 'Procedure 2'},
                        'toolLink': {'text': {'ja': 'リンク2', 'en': 'Link2'}, 'url': {'ja': 'http://example2.com', 'en': 'http://example2.com'}}
                    }
                }
            ]
        }
        
        result = processor._extract_procedures(condition)
        
        assert len(result) == 2
        assert result[0]['id'] == 'proc1'
        assert result[1]['id'] == 'proc2'
    
    def test_process_generated_data_fields_no_conditions(self):
        """Test _process_generated_data_fields with no conditions."""
        processor = DataProcessor()
        
        check = {
            'platform': ['web']
        }
        
        processor._process_generated_data_fields(check)
        
        # Should fall back to standard fields processing
        assert check['webConditionStatement'] == ""
        assert check['isSubcheck'] is False
        assert check['subchecks'] == {}
    
    def test_process_generated_data_fields_with_condition_statements(self):
        """Test _process_generated_data_fields with condition statements."""
        processor = DataProcessor()
        
        check = {
            'platform': ['web'],
            'target': 'design',
            'conditionStatements': [
                {
                    'platform': 'web',
                    'summary': {'ja': 'テスト条件', 'en': 'test condition'}
                }
            ],
            'conditions': []
        }
        
        processor._process_generated_data_fields(check)
        
        expected_statement = {
            'ja': 'テスト条件ことを確認する。',
            'en': 'Verify that test condition.'
        }
        assert check['webConditionStatement'] == expected_statement
    
    def test_process_generated_data_fields_single_procedure(self):
        """Test _process_generated_data_fields with single procedure."""
        processor = DataProcessor()
        
        check = {
            'platform': ['web'],
            'target': 'design',
            'conditions': [
                {
                    'platform': 'web',
                    'type': 'simple',
                    'procedure': {
                        'id': 'proc1',
                        'platform': 'web',
                        'target': 'design',
                        'tool': 'manual',
                        'procedure': {'ja': '手順テスト', 'en': 'Test procedure'},
                        'toolLink': {'text': {'ja': 'ツール', 'en': 'Tool'}, 'url': {'ja': 'http://tool.com', 'en': 'http://tool.com'}}
                    }
                }
            ]
        }
        
        processor._process_generated_data_fields(check)
        
        assert check['webConditionStatement'] == {'ja': '手順テスト', 'en': 'Test procedure'}
        assert check['webTools'] == [{'text': {'ja': 'ツール', 'en': 'Tool'}, 'url': {'ja': 'http://tool.com', 'en': 'http://tool.com'}}]
        assert check['isSubcheck'] is False
    
    def test_process_multiple_procedures(self):
        """Test _process_multiple_procedures method."""
        processor = DataProcessor()
        
        check = {
            'target': 'design',
            'subchecks': {
                'designWeb': {
                    'count': 0,
                    'conditions': []
                }
            }
        }
        
        condition = {
            'platform': 'web',
            'target': 'designWeb'
        }
        
        procedures = [
            {
                'id': 'proc1',
                'platform': 'web',
                'target': 'design',
                'tool': 'manual',
                'procedure': {'ja': '手順1', 'en': 'Procedure 1'},
                'toolLink': {'text': {'ja': 'ツール1', 'en': 'Tool1'}, 'url': {'ja': 'http://tool1.com', 'en': 'http://tool1.com'}}
            },
            {
                'id': 'proc2',
                'platform': 'web',
                'target': 'design',
                'tool': 'manual',
                'procedure': {'ja': '手順2', 'en': 'Procedure 2'},
                'toolLink': {'text': {'ja': 'ツール2', 'en': 'Tool2'}, 'url': {'ja': 'http://tool2.com', 'en': 'http://tool2.com'}}
            }
        ]
        
        processor._process_multiple_procedures(check, condition, procedures)
        
        # Check subchecks structure
        assert 'designWeb' in check['subchecks']
        assert len(check['subchecks']['designWeb']['conditions']) == 2
        
        # Check first subcheck
        subcheck1 = check['subchecks']['designWeb']['conditions'][0]
        assert subcheck1['id'] == 'proc1'
        assert subcheck1['checkId'] == ""
        assert subcheck1['subcheckId'] == 'proc1'
        assert subcheck1['isSubcheck'] is True
        assert subcheck1['webConditionStatement'] == {'ja': '手順1', 'en': 'Procedure 1'}
        assert subcheck1['webTools'] == [{'text': {'ja': 'ツール1', 'en': 'Tool1'}, 'url': {'ja': 'http://tool1.com', 'en': 'http://tool1.com'}}]
    
    def test_record_check_info_basic(self):
        """Test _record_check_info with basic check."""
        processor = DataProcessor()
        
        check = {
            'id': 'check1',
            'isSubcheck': False
        }
        
        processor._record_check_info(check)
        
        assert 'check1' in processor.check_info
        check_info = processor.check_info['check1']
        assert check_info.id == 'check1'
        assert check_info.is_subcheck is False
        assert check_info.subchecks_by_target == {}
    
    def test_record_check_info_with_subchecks(self):
        """Test _record_check_info with subchecks."""
        processor = DataProcessor()
        
        check = {
            'id': 'check1',
            'isSubcheck': True,
            'subchecks': {
                'designWeb': {'count': 3, 'conditions': []},
                'productIos': {'count': 2, 'conditions': []}
            }
        }
        
        processor._record_check_info(check)
        
        check_info = processor.check_info['check1']
        assert check_info.id == 'check1'
        assert check_info.is_subcheck is True
        assert check_info.subchecks_by_target == {
            'designWeb': 3,
            'productIos': 2
        }
    
    def test_record_check_info_invalid_subchecks(self):
        """Test _record_check_info with invalid subchecks structure."""
        processor = DataProcessor()
        
        check = {
            'id': 'check1',
            'isSubcheck': False,
            'subchecks': {
                'designWeb': 'invalid_structure'  # Not a dict with 'count'
            }
        }
        
        processor._record_check_info(check)
        
        check_info = processor.check_info['check1']
        assert check_info.subchecks_by_target == {}
    
    def test_distribute_to_sheets(self):
        """Test _distribute_to_sheets method."""
        processor = DataProcessor()
        
        processed_data = {
            'designWeb': [],
            'productIos': [],
            'unknownSheet': []
        }
        
        check = {
            'id': 'check1',
            'sheetNames': ['designWeb', 'productIos', 'unknownSheet'],
            'subchecks': {
                'designWeb': {
                    'conditions': [
                        {'id': 'sub1', 'subcheckId': 'sub1'},
                        {'id': 'sub2', 'subcheckId': 'sub2'}
                    ]
                }
            }
        }
        
        processor._distribute_to_sheets(check, processed_data)
        
        # Check main check distribution
        assert len(processed_data['designWeb']) == 3  # 1 main + 2 subchecks
        assert len(processed_data['productIos']) == 1  # 1 main only
        assert len(processed_data['unknownSheet']) == 1  # 1 main only
        
        # Check that subchecks were added to designWeb
        assert processed_data['designWeb'][0] == check
        assert processed_data['designWeb'][1]['id'] == 'sub1'
        assert processed_data['designWeb'][2]['id'] == 'sub2'
    
    def test_distribute_to_sheets_no_subchecks(self):
        """Test _distribute_to_sheets with no subchecks."""
        processor = DataProcessor()
        
        processed_data = {
            'designWeb': [],
            'productIos': []
        }
        
        check = {
            'id': 'check1',
            'sheetNames': ['designWeb', 'productIos']
        }
        
        processor._distribute_to_sheets(check, processed_data)
        
        # Only main checks should be added
        assert len(processed_data['designWeb']) == 1
        assert len(processed_data['productIos']) == 1
        assert processed_data['designWeb'][0] == check
        assert processed_data['productIos'][0] == check
    
    def test_distribute_to_sheets_missing_sheet(self):
        """Test _distribute_to_sheets with missing sheet in processed_data."""
        processor = DataProcessor()
        
        processed_data = {
            'designWeb': []
            # Missing 'productIos'
        }
        
        check = {
            'id': 'check1',
            'sheetNames': ['designWeb', 'productIos']
        }
        
        processor._distribute_to_sheets(check, processed_data)
        
        # Should only add to existing sheets
        assert len(processed_data['designWeb']) == 1
        assert 'productIos' not in processed_data
    
    def test_integration_complex_check_processing(self):
        """Integration test with complex check data."""
        processor = DataProcessor()
        
        source_data = {
            'complex_check': {
                'id': 'complex_check',
                'sortKey': 1,
                'target': 'product',
                'platform': ['web', 'ios'],
                'check': {'ja': '複雑なチェック', 'en': 'Complex check'},
                'severity': 'high',
                'conditionStatements': [
                    {
                        'platform': 'web',
                        'summary': {'ja': 'Web条件', 'en': 'Web condition'}
                    },
                    {
                        'platform': 'ios',
                        'summary': {'ja': 'iOS条件', 'en': 'iOS condition'}
                    }
                ],
                'conditions': [
                    {
                        'platform': 'web',
                        'type': 'complex',
                        'conditions': [
                            {
                                'type': 'simple',
                                'procedure': {
                                    'id': 'web_proc1',
                                    'platform': 'web',
                                    'target': 'product',
                                    'tool': 'manual',
                                    'procedure': {'ja': 'Web手順1', 'en': 'Web procedure 1'},
                                    'toolLink': {'text': {'ja': 'Webツール1', 'en': 'Web tool 1'}, 'url': {'ja': 'http://webtool1.com', 'en': 'http://webtool1.com'}}
                                }
                            },
                            {
                                'type': 'simple',
                                'procedure': {
                                    'id': 'web_proc2',
                                    'platform': 'web',
                                    'target': 'product',
                                    'tool': 'automated',
                                    'procedure': {'ja': 'Web手順2', 'en': 'Web procedure 2'},
                                    'toolLink': {'text': {'ja': 'Webツール2', 'en': 'Web tool 2'}, 'url': {'ja': 'http://webtool2.com', 'en': 'http://webtool2.com'}}
                                }
                            }
                        ]
                    },
                    {
                        'platform': 'ios',
                        'type': 'simple',
                        'procedure': {
                            'id': 'ios_proc1',
                            'platform': 'ios',
                            'target': 'product',
                            'tool': 'manual',
                            'procedure': {'ja': 'iOS手順1', 'en': 'iOS procedure 1'},
                            'toolLink': {'text': {'ja': 'iOSツール1', 'en': 'iOS tool 1'}, 'url': {'ja': 'http://iostool1.com', 'en': 'http://iostool1.com'}}
                        }
                    }
                ]
            }
        }
        
        result = processor.process_source_data(source_data)
        
        # Check that data was distributed correctly
        assert len(result['productWeb']) == 3  # 1 main + 2 subchecks
        assert len(result['productIos']) == 1  # 1 main only (single procedure)
        
        # Check main check in productWeb
        main_check_web = result['productWeb'][0]
        assert main_check_web['id'] == 'complex_check'
        assert main_check_web['checkId'] == 'complex_check'
        assert main_check_web['subcheckId'] == ""
        
        # Check subchecks in productWeb
        subcheck1 = result['productWeb'][1]
        assert subcheck1['id'] == 'web_proc1'
        assert subcheck1['subcheckId'] == 'web_proc1'
        assert subcheck1['isSubcheck'] is True
        
        subcheck2 = result['productWeb'][2]
        assert subcheck2['id'] == 'web_proc2'
        assert subcheck2['subcheckId'] == 'web_proc2'
        assert subcheck2['isSubcheck'] is True
        
        # Check main check in productIos (single procedure, no subchecks)
        main_check_ios = result['productIos'][0]
        assert main_check_ios['id'] == 'complex_check'
        assert main_check_ios['isSubcheck'] is False
        assert main_check_ios['iosConditionStatement'] == {'ja': 'iOS手順1', 'en': 'iOS procedure 1'}
        
        # Check that check_info was recorded
        assert 'complex_check' in processor.check_info
        check_info = processor.check_info['complex_check']
        assert check_info.subchecks_by_target['productWeb'] == 2
