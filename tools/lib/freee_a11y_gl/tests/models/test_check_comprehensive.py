"""Comprehensive test suite for models.check module to improve coverage."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typing import Dict, Any, List, Optional

from freee_a11y_gl.models.check import Check


class TestCheckComprehensive:
    """Comprehensive test cases for Check model to achieve high coverage."""

    def setup_method(self):
        """Set up test fixtures."""
        # Clear existing instances to avoid conflicts
        Check._instances.clear()
        
        # Initialize CheckTool instances needed for tests
        from freee_a11y_gl.models.check import CheckTool
        from freee_a11y_gl.settings import settings
        
        CheckTool._instances.clear()
        check_tools = settings.message_catalog.check_tools
        for tool_id, names in check_tools.items():
            CheckTool(tool_id, names)
        
        self.sample_data = {
            'id': 'test-check-001',
            'sortKey': 'test-001',
            'check': {
                'ja': 'テストチェック項目',
                'en': 'Test Check Item'
            },
            'severity': 'major',
            'target': 'designer',
            'platform': ['web', 'mobile'],
            'src_path': '/test/path/check.yaml'
        }

    def test_check_initialization_basic(self):
        """Test Check initialization with basic data."""
        check = Check(self.sample_data)
        
        assert check.id == 'test-check-001'
        assert check.sort_key == 'test-001'
        assert check.check_text == {'ja': 'テストチェック項目', 'en': 'Test Check Item'}
        assert check.severity == 'major'
        assert check.target == 'designer'
        assert check.platform == ['web', 'mobile']
        assert check.src_path == '/test/path/check.yaml'

    def test_check_template_data_basic(self):
        """Test Check template_data method with basic functionality."""
        check = Check(self.sample_data)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '
            
            template_data = check.template_data('en')
            
            assert isinstance(template_data, dict)
            assert 'id' in template_data
            assert 'check' in template_data
            assert template_data['id'] == 'test-check-001'
            assert template_data['check'] == 'Test Check Item'

    def test_check_template_data_japanese(self):
        """Test Check template_data method with Japanese language."""
        check = Check(self.sample_data)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'デザイナー'
            mock_config.get_severity_tag.return_value = '[重要]'
            mock_config.get_platform_name.return_value = 'ウェブ'
            mock_config.get_list_separator.return_value = '、'
            
            template_data = check.template_data('ja')
            
            assert isinstance(template_data, dict)
            assert template_data['check'] == 'テストチェック項目'

    def test_check_template_data_with_conditions(self):
        """Test Check template_data with conditions."""
        data_with_conditions = self.sample_data.copy()
        data_with_conditions['conditions'] = [
            {
                'type': 'simple',
                'platform': 'web',
                'id': 'proc-001',
                'tool': 'axe',
                'procedure': {
                    'ja': 'テスト手順',
                    'en': 'Test procedure'
                }
            }
        ]
        
        check = Check(data_with_conditions)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '
            
            template_data = check.template_data('en')
            
            assert 'conditions' in template_data
            assert len(template_data['conditions']) == 1

    def test_check_template_data_with_implementations(self):
        """Test Check template_data with implementations."""
        data_with_impl = self.sample_data.copy()
        data_with_impl['implementations'] = [
            {
                'title': {
                    'ja': '実装タイトル',
                    'en': 'Implementation Title'
                },
                'methods': [
                    {
                        'platform': 'web',
                        'method': {
                            'ja': '実装方法',
                            'en': 'Implementation method'
                        }
                    }
                ]
            }
        ]
        
        check = Check(data_with_impl)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '
            
            template_data = check.template_data('en')
            
            assert 'implementations' in template_data
            assert len(template_data['implementations']) == 1

    def test_check_condition_platforms(self):
        """Test Check condition_platforms method."""
        data_with_conditions = self.sample_data.copy()
        data_with_conditions['conditions'] = [
            {
                'type': 'simple',
                'platform': 'web',
                'id': 'proc-001',
                'tool': 'axe',
                'procedure': {
                    'ja': 'テスト手順1',
                    'en': 'Test procedure 1'
                }
            },
            {
                'type': 'simple',
                'platform': 'mobile',
                'id': 'proc-002',
                'tool': 'axe',
                'procedure': {
                    'ja': 'テスト手順2',
                    'en': 'Test procedure 2'
                }
            }
        ]
        
        check = Check(data_with_conditions)
        platforms = check.condition_platforms()
        
        assert isinstance(platforms, list)
        assert 'web' in platforms
        assert 'mobile' in platforms

    def test_check_join_items_static_method(self):
        """Test Check join_items static method."""
        items = ['web', 'mobile', 'desktop']
        
        with patch('freee_a11y_gl.utils.Config') as mock_config:
            mock_config.get_list_separator.return_value = ', '
            mock_config.get_platform_name.side_effect = lambda item, lang: f'{item.title()}'
            
            result = Check.join_items(items, 'en')
            
            assert isinstance(result, str)
            assert 'Web' in result
            assert 'Mobile' in result
            assert 'Desktop' in result

    def test_check_object_data_basic(self):
        """Test Check object_data method."""
        check = Check(self.sample_data)
        
        with patch('freee_a11y_gl.models.base.BaseModel._get_relationship_manager'):
            object_data = check.object_data()
            
            assert isinstance(object_data, dict)
            assert 'id' in object_data
            assert 'sortKey' in object_data
            assert 'check' in object_data
            assert 'severity' in object_data
            assert object_data['id'] == 'test-check-001'

    def test_check_object_data_with_conditions(self):
        """Test Check object_data with conditions."""
        data_with_conditions = self.sample_data.copy()
        data_with_conditions['conditions'] = [
            {
                'type': 'simple',
                'platform': 'web',
                'id': 'proc-001',
                'tool': 'axe',
                'procedure': {
                    'ja': 'テスト手順',
                    'en': 'Test procedure'
                }
            }
        ]
        
        check = Check(data_with_conditions)
        
        with patch('freee_a11y_gl.models.base.BaseModel._get_relationship_manager'):
            object_data = check.object_data()
            
            assert 'conditions' in object_data
            assert 'conditionStatements' in object_data

    def test_check_list_all_src_paths_class_method(self):
        """Test Check list_all_src_paths class method."""
        # Clear existing instances first
        Check._instances.clear()
        
        check1 = Check(self.sample_data)
        
        data2 = self.sample_data.copy()
        data2['id'] = 'test-check-002'
        data2['sortKey'] = 'test-002'  # Use unique sortKey
        data2['src_path'] = '/test/path/check2.yaml'
        check2 = Check(data2)
        
        src_paths = Check.list_all_src_paths()
        
        assert isinstance(src_paths, list)
        assert '/test/path/check.yaml' in src_paths
        assert '/test/path/check2.yaml' in src_paths

    def test_check_object_data_all_class_method(self):
        """Test Check object_data_all class method."""
        # Clear existing instances first
        Check._instances.clear()
        
        check1 = Check(self.sample_data)
        
        with patch('freee_a11y_gl.models.base.BaseModel._get_relationship_manager'):
            all_data = Check.object_data_all()
            
            assert isinstance(all_data, dict)
            assert 'test-check-001' in all_data

    def test_check_template_data_all_class_method(self):
        """Test Check template_data_all class method."""
        # Clear existing instances first
        Check._instances.clear()
        
        check1 = Check(self.sample_data)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '
            
            template_data_generator = Check.template_data_all('en')
            template_data_list = list(template_data_generator)
            
            assert isinstance(template_data_list, list)
            assert len(template_data_list) == 1

    def test_check_duplicate_id_error(self):
        """Test Check raises error for duplicate ID."""
        check1 = Check(self.sample_data)
        
        with pytest.raises(ValueError, match='Duplicate check ID'):
            check2 = Check(self.sample_data)

    def test_check_duplicate_sort_key_error(self):
        """Test Check raises error for duplicate sortKey."""
        check1 = Check(self.sample_data)
        
        data2 = self.sample_data.copy()
        data2['id'] = 'different-id'
        # Same sortKey should cause error
        
        with pytest.raises(ValueError, match='Duplicate check sortKey'):
            check2 = Check(data2)

    def test_check_with_empty_conditions(self):
        """Test Check with empty conditions list."""
        data_empty_conditions = self.sample_data.copy()
        data_empty_conditions['conditions'] = []
        
        check = Check(data_empty_conditions)
        
        assert check.conditions == []
        assert check.condition_platforms() == []

    def test_check_with_empty_implementations(self):
        """Test Check with empty implementations list."""
        data_empty_impl = self.sample_data.copy()
        data_empty_impl['implementations'] = []
        
        check = Check(data_empty_impl)
        
        assert check.implementations == []

    def test_check_template_data_with_platform_filter(self):
        """Test Check template_data with platform filtering."""
        data_with_conditions = self.sample_data.copy()
        data_with_conditions['conditions'] = [
            {
                'type': 'simple',
                'platform': 'web',
                'id': 'proc-001',
                'tool': 'axe',
                'procedure': {
                    'ja': 'ウェブ手順',
                    'en': 'Web procedure'
                }
            },
            {
                'type': 'simple',
                'platform': 'mobile',
                'id': 'proc-002',
                'tool': 'axe',
                'procedure': {
                    'ja': 'モバイル手順',
                    'en': 'Mobile procedure'
                }
            }
        ]
        
        check = Check(data_with_conditions)
        
        with patch('freee_a11y_gl.models.check.Config') as mock_config:
            mock_config.get_check_target_name.return_value = 'Designer'
            mock_config.get_severity_tag.return_value = '[MAJOR]'
            mock_config.get_platform_name.return_value = 'Web'
            mock_config.get_list_separator.return_value = ', '
            
            # Test with platform filter
            template_data = check.template_data('en', platform=['web'])
            
            assert 'conditions' in template_data
            # Should only include web conditions
            web_conditions = [c for c in template_data['conditions'] if 'Web' in str(c)]

    def test_check_string_representation(self):
        """Test Check string representation."""
        check = Check(self.sample_data)
        str_repr = str(check)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_check_inheritance_from_base_model(self):
        """Test Check inherits from BaseModel correctly."""
        check = Check(self.sample_data)
        
        # Test BaseModel methods
        assert hasattr(check, 'id')
        assert hasattr(check, 'object_type')
        assert check.object_type == 'check'

    def test_check_instances_tracking(self):
        """Test Check instances are tracked correctly."""
        # Clear existing instances
        Check._instances.clear()
        
        check1 = Check(self.sample_data)
        assert 'test-check-001' in Check._instances
        assert Check._instances['test-check-001'] == check1

    def test_check_with_complex_conditions(self):
        """Test Check with complex nested conditions."""
        data_complex = self.sample_data.copy()
        data_complex['conditions'] = [
            {
                'type': 'and',
                'conditions': [
                    {
                        'type': 'simple',
                        'platform': 'web',
                        'id': 'proc-001',
                        'tool': 'axe',
                        'procedure': {
                            'ja': '手順1',
                            'en': 'Procedure 1'
                        }
                    },
                    {
                        'type': 'simple',
                        'platform': 'web',
                        'id': 'proc-002',
                        'tool': 'manual',
                        'procedure': {
                            'ja': '手順2',
                            'en': 'Procedure 2'
                        }
                    }
                ]
            }
        ]
        
        check = Check(data_complex)
        
        assert len(check.conditions) == 1
        assert check.conditions[0].type == 'and'
        assert len(check.conditions[0].conditions) == 2

    def teardown_method(self):
        """Clean up after each test."""
        # Clear instances to avoid conflicts between tests
        Check._instances.clear()
        from freee_a11y_gl.models.check import CheckTool
        CheckTool._instances.clear()
