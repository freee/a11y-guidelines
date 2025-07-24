"""
Integration tests for YAML validation in initializer.
"""

import json
import os
import tempfile
import unittest
import yaml
from unittest.mock import patch

from freee_a11y_gl.initializer import setup_instances
from freee_a11y_gl.yaml_validator import ValidationError


class TestInitializerValidation(unittest.TestCase):
    """Test cases for YAML validation integration in initializer"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory structure
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
        
        # Create minimal schema files
        common_schema = {
            "$id": "https://a11y-guidelines.freee.co.jp/schemas/common.json",
            "type": "object",
            "$defs": {
                "i18nString": {
                    "type": "object",
                    "properties": {
                        "ja": {"type": "string"},
                        "en": {"type": "string"}
                    },
                    "additionalProperties": False,
                    "required": ["ja", "en"]
                }
            }
        }
        
        check_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://a11y-guidelines.freee.co.jp/schemas/check.json",
            "title": "check",
            "type": "object",
            "properties": {
                "id": {"type": "string", "pattern": "^[0-9]{4}"},
                "sortKey": {"type": "integer"},
                "check": {"$ref": "common.json#/$defs/i18nString"},
                "severity": {"enum": ["critical", "major", "normal", "minor"]},
                "target": {"enum": ["design", "code", "product"]},
                "platform": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"enum": ["web", "mobile"]}
                }
            },
            "additionalProperties": False,
            "required": ["id", "sortKey", "check", "severity", "target", "platform"]
        }
        
        # Write schema files
        with open(os.path.join(self.schemas_dir, 'common.json'), 'w') as f:
            json.dump(common_schema, f)
        
        with open(os.path.join(self.schemas_dir, 'check.json'), 'w') as f:
            json.dump(check_schema, f)
        
        # Create minimal schemas for other types to avoid warnings
        for schema_name in ['guideline.json', 'faq.json']:
            with open(os.path.join(self.schemas_dir, schema_name), 'w') as f:
                json.dump({"type": "object"}, f)
        
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

    def create_valid_check_yaml(self, filename='0001.yaml'):
        """Create a valid check YAML file"""
        valid_check = {
            'id': '0001',
            'sortKey': 100000,
            'check': {
                'ja': '有効なチェック項目',
                'en': 'Valid check item'
            },
            'severity': 'normal',
            'target': 'design',
            'platform': ['web', 'mobile']
        }
        
        filepath = os.path.join(self.yaml_dir, 'checks', filename)
        with open(filepath, 'w') as f:
            yaml.dump(valid_check, f)
        
        return filepath

    def create_invalid_check_yaml(self, filename='0002.yaml'):
        """Create an invalid check YAML file"""
        invalid_check = {
            'id': '0002',
            'check': {
                'ja': '無効なチェック項目'
                # Missing required 'en' field
            },
            'severity': 'normal',
            'target': 'design',
            'platform': ['web', 'mobile']
        }
        
        filepath = os.path.join(self.yaml_dir, 'checks', filename)
        with open(filepath, 'w') as f:
            yaml.dump(invalid_check, f)
        
        return filepath

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    def test_setup_instances_with_valid_yaml(self, mock_rel_manager, mock_axe_rules):
        """Test setup_instances with valid YAML files"""
        # Create valid YAML file
        self.create_valid_check_yaml()
        
        # Mock the axe rules processing and relationship manager
        mock_axe_rules.return_value = None
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        # This should not raise any exception
        try:
            result = setup_instances(self.temp_dir)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"setup_instances raised an exception unexpectedly: {e}")

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    @patch('sys.exit')
    def test_setup_instances_with_invalid_yaml(self, mock_exit, mock_rel_manager, mock_axe_rules):
        """Test setup_instances with invalid YAML files"""
        # Create invalid YAML file
        self.create_invalid_check_yaml()
        
        # Mock the axe rules processing and relationship manager
        mock_axe_rules.return_value = None
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        # This should call sys.exit(1) due to validation error
        setup_instances(self.temp_dir)
        
        # Verify that sys.exit was called with code 1
        mock_exit.assert_called_with(1)

    @patch('freee_a11y_gl.initializer.process_axe_rules')
    @patch('freee_a11y_gl.initializer.RelationshipManager')
    def test_setup_instances_with_mixed_yaml(self, mock_rel_manager, mock_axe_rules):
        """Test setup_instances with both valid and invalid YAML files"""
        # Create both valid and invalid YAML files
        self.create_valid_check_yaml('0001.yaml')
        self.create_invalid_check_yaml('0002.yaml')
        
        # Mock the axe rules processing and relationship manager
        mock_axe_rules.return_value = None
        mock_rel_instance = mock_rel_manager.return_value
        mock_rel_instance.resolve_faqs.return_value = None
        
        # This should exit due to the invalid file
        with patch('sys.exit') as mock_exit:
            setup_instances(self.temp_dir)
            mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
