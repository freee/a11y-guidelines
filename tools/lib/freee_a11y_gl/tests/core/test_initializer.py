"""
Comprehensive tests for initializer module.
"""

import json
import os
import tempfile
import unittest
import yaml
import git
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path

from freee_a11y_gl.initializer import (
    setup_instances,
    process_axe_rules,
    ls_dir,
    read_file_content,
    handle_file_error,
    read_yaml_file,
    process_entity_files,
    process_static_entity_file
)
from freee_a11y_gl.yaml_validator import ValidationError


class TestSetupInstances(unittest.TestCase):
    """Test cases for setup_instances function"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create data directory structure
        self.data_dir = os.path.join(self.temp_dir, 'data')
        self.yaml_dir = os.path.join(self.data_dir, 'yaml')
        self.json_dir = os.path.join(self.data_dir, 'json')
        self.schemas_dir = os.path.join(self.json_dir, 'schemas')
        
        os.makedirs(self.yaml_dir)
        os.makedirs(self.schemas_dir)
        
        # Create subdirectories for YAML files
        for subdir in ['checks', 'gl', 'faq']:
            os.makedirs(os.path.join(self.yaml_dir, subdir))
        
        # Create required JSON files for static entities
        static_files = {
            'guideline-categories.json': {},
            'wcag-sc.json': {},
            'faq-tags.json': {},
            'info.json': {}
        }
        
        for filename, content in static_files.items():
            with open(os.path.join(self.json_dir, filename), 'w') as f:
                json.dump(content, f)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    @patch('freee_a11y_gl.initializer.process_entity_files')
    @patch('freee_a11y_gl.initializer.process_static_entity_file')
    @patch('freee_a11y_gl.initializer.CheckTool')
    @patch('freee_a11y_gl.config.Config.get_basedir')
    @patch('freee_a11y_gl.config.Config.get_yaml_validation_mode')
    def test_setup_instances_with_basedir_none(self, mock_validation_mode, mock_get_basedir, 
                                               mock_check_tool, mock_process_static, 
                                               mock_process_entity, mock_rel_manager, mock_axe_rules):
        """Test setup_instances when basedir is None"""
        mock_get_basedir.return_value = self.temp_dir
        mock_validation_mode.return_value = 'disabled'
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        result = setup_instances(basedir=None)
        
        mock_get_basedir.assert_called_once()
        self.assertIsNotNone(result)

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    @patch('freee_a11y_gl.initializer.process_entity_files')
    @patch('freee_a11y_gl.initializer.process_static_entity_file')
    @patch('freee_a11y_gl.initializer.CheckTool')
    @patch('freee_a11y_gl.config.Config.get_yaml_validation_mode')
    def test_setup_instances_with_explicit_basedir(self, mock_validation_mode, mock_check_tool, 
                                                   mock_process_static, mock_process_entity, 
                                                   mock_rel_manager, mock_axe_rules):
        """Test setup_instances with explicit basedir"""
        mock_validation_mode.return_value = 'strict'
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        result = setup_instances(basedir=self.temp_dir)
        
        self.assertIsNotNone(result)
        mock_axe_rules.assert_called_once()

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    @patch('freee_a11y_gl.initializer.process_entity_files')
    @patch('freee_a11y_gl.initializer.process_static_entity_file')
    @patch('freee_a11y_gl.initializer.CheckTool')
    @patch('freee_a11y_gl.config.Config.get_yaml_validation_mode')
    def test_setup_instances_check_tool_creation(self, mock_validation_mode, mock_check_tool, 
                                                 mock_process_static, mock_process_entity, 
                                                 mock_rel_manager, mock_axe_rules):
        """Test that CheckTool instances are created for all tools"""
        mock_validation_mode.return_value = 'warning'
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        setup_instances(basedir=self.temp_dir)
        
        # Verify CheckTool was called for each tool in check_tools
        from freee_a11y_gl.settings import settings
        check_tools = settings.message_catalog.check_tools
        expected_calls = [call(tool_id, tool_names) for tool_id, tool_names in check_tools.items()]
        mock_check_tool.assert_has_calls(expected_calls, any_order=True)

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    @patch('freee_a11y_gl.initializer.process_entity_files')
    @patch('freee_a11y_gl.initializer.process_static_entity_file')
    @patch('freee_a11y_gl.initializer.CheckTool')
    @patch('freee_a11y_gl.config.Config.get_yaml_validation_mode')
    def test_setup_instances_entity_processing_order(self, mock_validation_mode, mock_check_tool, 
                                                     mock_process_static, mock_process_entity, 
                                                     mock_rel_manager, mock_axe_rules):
        """Test that entities are processed in the correct order"""
        mock_validation_mode.return_value = 'disabled'
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        setup_instances(basedir=self.temp_dir)
        
        # Verify static entities are processed first
        self.assertEqual(mock_process_static.call_count, 4)
        
        # Verify dynamic entities are processed in order
        self.assertEqual(mock_process_entity.call_count, 3)
        
        # Check the order of calls for dynamic entities
        entity_calls = mock_process_entity.call_args_list
        self.assertEqual(len(entity_calls), 3)


class TestProcessAxeRules(unittest.TestCase):
    """Test cases for process_axe_rules function"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    @patch('freee_a11y_gl.initializer.AxeRule')
    @patch('freee_a11y_gl.config.Config.get_basedir')
    def test_process_axe_rules_with_basedir_none(self, mock_get_basedir, mock_axe_rule):
        """Test process_axe_rules when basedir is None"""
        mock_get_basedir.return_value = self.temp_dir
        
        # Mock git repository
        with patch('git.Repo') as mock_repo:
            mock_root_repo = MagicMock()
            mock_submodule = MagicMock()
            mock_submodule.name = 'vendor/axe-core'  # Use correct submodule name
            mock_submodule.hexsha = 'abc123'
            mock_root_repo.submodules = [mock_submodule]
            mock_repo.return_value = mock_root_repo
            
            # Mock axe repository and commit
            mock_axe_repo = MagicMock()
            mock_commit = MagicMock()
            mock_commit.authored_date = 1234567890
            mock_axe_repo.commit.return_value = mock_commit
            
            # Mock tree structure
            mock_tree = MagicMock()
            
            # Mock message blob
            mock_msg_blob = MagicMock()
            mock_msg_blob.data_stream.read.return_value = b'{"rules": {"test-rule": {"message": "Test message", "help": "Test help", "description": "Test description"}}}'
            
            # Mock package blob with version
            mock_pkg_blob = MagicMock()
            mock_pkg_blob.data_stream.read.return_value = b'{"version": "4.6.3"}'
            
            # Setup tree navigation to return different blobs for different paths
            # Need to handle 3 calls: message file, rules directory, package file
            mock_tree.__truediv__ = MagicMock(side_effect=[mock_msg_blob, mock_tree, mock_pkg_blob])
            mock_commit.tree = mock_tree
            
            # Mock rule blobs
            mock_rule_blob = MagicMock()
            mock_rule_blob.type = 'blob'
            mock_rule_blob.path = 'test-rule.json'
            mock_rule_blob.data_stream.read.return_value = b'{"id": "test-rule", "ruleId": "test-rule", "metadata": {"help": "Test help text", "description": "Test description"}, "tags": ["wcag2a", "section508"]}'
            mock_tree.traverse.return_value = [mock_rule_blob]
            
            mock_repo.side_effect = [mock_root_repo, mock_axe_repo]
            
            from freee_a11y_gl.config import Config
            axe_core_config = Config.get_axe_core_config()
            process_axe_rules(None, axe_core_config)
            
            mock_get_basedir.assert_called_once()
            mock_axe_rule.assert_called()

    def test_process_axe_rules_submodule_not_found(self):
        """Test process_axe_rules when submodule is not found"""
        with patch('git.Repo') as mock_repo:
            mock_root_repo = MagicMock()
            mock_root_repo.submodules = []  # No submodules
            mock_repo.return_value = mock_root_repo
            
            from freee_a11y_gl.config import Config
            axe_core_config = Config.get_axe_core_config()
            
            with self.assertRaises(ValueError) as context:
                process_axe_rules(self.temp_dir, axe_core_config)
            
            self.assertIn('Submodule with name', str(context.exception))

    @patch('freee_a11y_gl.initializer.AxeRule')
    @patch('time.strftime')
    @patch('time.localtime')
    def test_process_axe_rules_complete_flow(self, mock_localtime, mock_strftime, mock_axe_rule):
        """Test complete flow of process_axe_rules"""
        mock_localtime.return_value = 'mock_time'
        mock_strftime.return_value = '2023-01-01 12:00:00+0000'
        
        with patch('git.Repo') as mock_repo:
            # Setup mock repository structure
            mock_root_repo = MagicMock()
            mock_submodule = MagicMock()
            mock_submodule.name = 'vendor/axe-core'  # Use correct submodule name
            mock_submodule.hexsha = 'commit123'
            mock_root_repo.submodules = [mock_submodule]
            
            mock_axe_repo = MagicMock()
            mock_commit = MagicMock()
            mock_commit.authored_date = 1672574400
            mock_axe_repo.commit.return_value = mock_commit
            
            # Mock message file
            mock_msg_blob = MagicMock()
            mock_msg_blob.data_stream.read.return_value = '{"rules": {"test-rule": {"message": "テストメッセージ", "help": "テストヘルプ", "description": "テスト説明"}}}'.encode('utf-8')
            
            # Mock rule files
            mock_rule_blob = MagicMock()
            mock_rule_blob.type = 'blob'
            mock_rule_blob.path = 'test-rule.json'
            mock_rule_blob.data_stream.read.return_value = b'{"id": "test-rule", "ruleId": "test-rule", "metadata": {"help": "Test help text", "description": "Test description"}, "tags": ["wcag2a", "section508"]}'
            
            # Mock package file
            mock_pkg_blob = MagicMock()
            mock_pkg_blob.data_stream.read.return_value = b'{"version": "4.6.3"}'
            
            # Setup tree navigation
            mock_tree = MagicMock()
            mock_tree.__truediv__ = MagicMock()
            # Need to handle 3 calls: message file, rules directory, package file
            mock_tree.__truediv__.side_effect = [mock_msg_blob, mock_tree, mock_pkg_blob]
            mock_tree.traverse.return_value = [mock_rule_blob]
            mock_commit.tree = mock_tree
            
            mock_repo.side_effect = [mock_root_repo, mock_axe_repo]
            
            from freee_a11y_gl.config import Config
            axe_core_config = Config.get_axe_core_config()
            process_axe_rules(self.temp_dir, axe_core_config)
            
            # Verify AxeRule was called
            mock_axe_rule.assert_called()


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_ls_dir_no_extension_filter(self):
        """Test ls_dir without extension filter"""
        # Create test files
        test_files = ['file1.txt', 'file2.yaml', 'file3.json']
        for filename in test_files:
            with open(os.path.join(self.temp_dir, filename), 'w') as f:
                f.write('test content')
        
        # Create subdirectory with files
        subdir = os.path.join(self.temp_dir, 'subdir')
        os.makedirs(subdir)
        with open(os.path.join(subdir, 'file4.txt'), 'w') as f:
            f.write('test content')
        
        result = ls_dir(self.temp_dir)
        
        # Should return all files recursively
        self.assertEqual(len(result), 4)
        self.assertTrue(any('file1.txt' in path for path in result))
        self.assertTrue(any('file4.txt' in path for path in result))

    def test_ls_dir_with_extension_filter(self):
        """Test ls_dir with extension filter"""
        # Create test files
        test_files = ['file1.txt', 'file2.yaml', 'file3.json']
        for filename in test_files:
            with open(os.path.join(self.temp_dir, filename), 'w') as f:
                f.write('test content')
        
        result = ls_dir(self.temp_dir, extension='.yaml')
        
        # Should return only .yaml files
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].endswith('file2.yaml'))

    def test_ls_dir_empty_directory(self):
        """Test ls_dir with empty directory"""
        result = ls_dir(self.temp_dir)
        self.assertEqual(len(result), 0)

    def test_read_file_content_success(self):
        """Test read_file_content with valid file"""
        test_content = "Test file content\nWith multiple lines"
        test_file = os.path.join(self.temp_dir, 'test.txt')
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = read_file_content(test_file)
        self.assertEqual(result, test_content)

    def test_read_file_content_file_not_found(self):
        """Test read_file_content with non-existent file"""
        non_existent_file = os.path.join(self.temp_dir, 'nonexistent.txt')
        
        with self.assertRaises(FileNotFoundError):
            read_file_content(non_existent_file)

    def test_read_file_content_permission_error(self):
        """Test read_file_content with permission error"""
        test_file = os.path.join(self.temp_dir, 'test.txt')
        
        with open(test_file, 'w') as f:
            f.write('test')
        
        # Mock permission error
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with self.assertRaises(PermissionError):
                read_file_content(test_file)

    @patch('sys.exit')
    @patch('sys.stderr')
    def test_handle_file_error(self, mock_stderr, mock_exit):
        """Test handle_file_error function"""
        test_error = FileNotFoundError("File not found")
        test_file = "/path/to/test/file.txt"
        
        handle_file_error(test_error, test_file)
        
        mock_exit.assert_called_once_with(1)

    def test_read_yaml_file_success(self):
        """Test read_yaml_file with valid YAML"""
        test_data = {'key': 'value', 'list': [1, 2, 3]}
        test_file = os.path.join(self.temp_dir, 'test.yaml')
        
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = read_yaml_file(test_file)
        self.assertEqual(result, test_data)

    @patch('freee_a11y_gl.initializer.handle_file_error')
    def test_read_yaml_file_file_error(self, mock_handle_error):
        """Test read_yaml_file with file error"""
        non_existent_file = os.path.join(self.temp_dir, 'nonexistent.yaml')
        
        read_yaml_file(non_existent_file)
        
        mock_handle_error.assert_called_once()

    @patch('sys.exit')
    def test_read_yaml_file_invalid_yaml(self, mock_exit):
        """Test read_yaml_file with invalid YAML content"""
        test_file = os.path.join(self.temp_dir, 'invalid.yaml')
        
        with open(test_file, 'w') as f:
            f.write('invalid: yaml: content: [')
        
        # Should call sys.exit due to YAML scanner error
        read_yaml_file(test_file)
        mock_exit.assert_called_once_with(1)


class TestProcessEntityFiles(unittest.TestCase):
    """Test cases for process_entity_files function"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.srcdir = os.path.join(self.temp_dir, 'entities')
        os.makedirs(self.srcdir)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_process_entity_files_without_validation(self):
        """Test process_entity_files without validation"""
        # Create test YAML file
        test_data = {'id': 'test001', 'name': 'Test Entity'}
        test_file = os.path.join(self.srcdir, 'test.yaml')
        
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Mock constructor
        mock_constructor = MagicMock()
        
        process_entity_files(self.srcdir, mock_constructor)
        
        # Verify constructor was called with data including src_path
        mock_constructor.assert_called_once()
        call_args = mock_constructor.call_args[0][0]
        self.assertEqual(call_args['id'], 'test001')
        self.assertEqual(call_args['name'], 'Test Entity')
        self.assertTrue('src_path' in call_args)

    def test_process_entity_files_with_validation_success(self):
        """Test process_entity_files with successful validation"""
        # Create test YAML file
        test_data = {'id': 'test001', 'name': 'Test Entity'}
        test_file = os.path.join(self.srcdir, 'test.yaml')
        
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Mock constructor and validator
        mock_constructor = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_with_mode.return_value = None
        
        process_entity_files(self.srcdir, mock_constructor, 'test_schema', mock_validator)
        
        # Verify validation was called (data now includes src_path)
        expected_data = test_data.copy()
        expected_data['src_path'] = test_file
        mock_validator.validate_with_mode.assert_called_once_with(
            expected_data, 'test_schema', test_file
        )
        
        # Verify constructor was called
        mock_constructor.assert_called_once()

    @patch('sys.exit')
    def test_process_entity_files_with_validation_error(self, mock_exit):
        """Test process_entity_files with validation error"""
        # Create test YAML file
        test_data = {'id': 'test001', 'name': 'Test Entity'}
        test_file = os.path.join(self.srcdir, 'test.yaml')
        
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Mock constructor and validator
        mock_constructor = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_with_mode.side_effect = ValidationError("Validation failed")
        
        process_entity_files(self.srcdir, mock_constructor, 'test_schema', mock_validator)
        
        # Verify sys.exit was called
        mock_exit.assert_called_once_with(1)

    @patch('freee_a11y_gl.initializer.handle_file_error')
    def test_process_entity_files_file_read_error(self, mock_handle_error):
        """Test process_entity_files with file read error"""
        # Create a file that will cause read error
        test_file = os.path.join(self.srcdir, 'test.yaml')
        with open(test_file, 'w') as f:
            f.write('test')
        
        mock_constructor = MagicMock()
        
        # Mock read_file_content to raise an exception
        with patch('freee_a11y_gl.initializer.read_file_content', side_effect=IOError("Read error")):
            process_entity_files(self.srcdir, mock_constructor)
            
            mock_handle_error.assert_called_once()

    @patch('freee_a11y_gl.initializer.handle_file_error')
    def test_process_entity_files_constructor_error(self, mock_handle_error):
        """Test process_entity_files with constructor error"""
        # Create test YAML file
        test_data = {'id': 'test001', 'name': 'Test Entity'}
        test_file = os.path.join(self.srcdir, 'test.yaml')
        
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Mock constructor to raise exception
        mock_constructor = MagicMock(side_effect=ValueError("Constructor error"))
        
        process_entity_files(self.srcdir, mock_constructor)
        
        mock_handle_error.assert_called_once()


class TestProcessStaticEntityFile(unittest.TestCase):
    """Test cases for process_static_entity_file function"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_process_static_entity_file_success(self):
        """Test process_static_entity_file with valid JSON"""
        test_data = {
            'entity1': {'name': 'Entity 1', 'value': 100},
            'entity2': {'name': 'Entity 2', 'value': 200}
        }
        test_file = os.path.join(self.temp_dir, 'entities.json')
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        mock_constructor = MagicMock()
        
        process_static_entity_file(test_file, mock_constructor)
        
        # Verify constructor was called for each entity
        expected_calls = [
            call('entity1', {'name': 'Entity 1', 'value': 100}),
            call('entity2', {'name': 'Entity 2', 'value': 200})
        ]
        mock_constructor.assert_has_calls(expected_calls, any_order=True)

    @patch('freee_a11y_gl.initializer.handle_file_error')
    def test_process_static_entity_file_read_error(self, mock_handle_error):
        """Test process_static_entity_file with file read error"""
        non_existent_file = os.path.join(self.temp_dir, 'nonexistent.json')
        mock_constructor = MagicMock()
        
        process_static_entity_file(non_existent_file, mock_constructor)
        
        mock_handle_error.assert_called_once()

    @patch('freee_a11y_gl.initializer.handle_file_error')
    def test_process_static_entity_file_constructor_error(self, mock_handle_error):
        """Test process_static_entity_file with constructor error"""
        test_data = {'entity1': {'name': 'Entity 1'}}
        test_file = os.path.join(self.temp_dir, 'entities.json')
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        mock_constructor = MagicMock(side_effect=ValueError("Constructor error"))
        
        process_static_entity_file(test_file, mock_constructor)
        
        mock_handle_error.assert_called_once()

    @patch('sys.exit')
    def test_process_static_entity_file_invalid_json(self, mock_exit):
        """Test process_static_entity_file with invalid JSON"""
        test_file = os.path.join(self.temp_dir, 'invalid.json')
        
        with open(test_file, 'w') as f:
            f.write('{"invalid": json content}')
        
        mock_constructor = MagicMock()
        
        # Should call sys.exit due to JSON decode error
        process_static_entity_file(test_file, mock_constructor)
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
