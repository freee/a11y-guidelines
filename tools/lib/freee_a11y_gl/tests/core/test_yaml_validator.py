"""
Tests for YAML validation functionality.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from freee_a11y_gl.yaml_validator import YamlValidator, ValidationError


class TestYamlValidator(unittest.TestCase):
    """Test cases for YamlValidator class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for schemas
        self.temp_dir = tempfile.mkdtemp()

        # Sample schemas for testing
        self.common_schema = {
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

        self.check_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://a11y-guidelines.freee.co.jp/schemas/check.json",
            "title": "check",
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^[0-9]{4}"
                },
                "check": {
                    "$ref": "common.json#/$defs/i18nString"
                },
                "severity": {
                    "enum": ["critical", "major", "normal", "minor"]
                },
                "target": {
                    "enum": ["design", "code", "product"]
                },
                "platform": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "enum": ["web", "mobile"]
                    }
                }
            },
            "additionalProperties": False,
            "required": ["id", "check", "severity", "target", "platform"]
        }

        # Write schema files
        with open(os.path.join(self.temp_dir, 'common.json'), 'w') as f:
            json.dump(self.common_schema, f)

        with open(os.path.join(self.temp_dir, 'check.json'), 'w') as f:
            json.dump(self.check_schema, f)

        # Create empty files for other schemas to avoid warnings
        for schema_name in ['guideline.json', 'faq.json']:
            with open(os.path.join(self.temp_dir, schema_name), 'w') as f:
                json.dump({"type": "object"}, f)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_validator_initialization(self):
        """Test validator initialization"""
        validator = YamlValidator(self.temp_dir)

        # Check that schemas are loaded
        self.assertIn('common', validator.schemas)
        self.assertIn('check', validator.schemas)
        self.assertIn('guideline', validator.schemas)
        self.assertIn('faq', validator.schemas)

        # Check that resolvers are created
        self.assertIn('common', validator.resolvers)
        self.assertIn('check', validator.resolvers)

    def test_get_available_schemas(self):
        """Test getting available schema names"""
        validator = YamlValidator(self.temp_dir)
        schemas = validator.get_available_schemas()

        expected_schemas = ['common', 'check', 'guideline', 'faq']
        for schema in expected_schemas:
            self.assertIn(schema, schemas)

    def test_valid_yaml_data(self):
        """Test validation with valid YAML data"""
        validator = YamlValidator(self.temp_dir)

        valid_data = {
            "id": "0001",
            "check": {
                "ja": "日本語のチェック内容",
                "en": "English check content"
            },
            "severity": "normal",
            "target": "design",
            "platform": ["web", "mobile"]
        }

        # Should not raise any exception
        try:
            validator.validate_yaml_data(valid_data, 'check', '/test/file.yaml')
        except ValidationError:
            self.fail("validate_yaml_data raised ValidationError unexpectedly")

    def test_invalid_yaml_data_missing_required(self):
        """Test validation with missing required fields"""
        validator = YamlValidator(self.temp_dir)

        invalid_data = {
            "id": "0001",
            "check": {
                "ja": "日本語のチェック内容",
                "en": "English check content"
            },
            "severity": "normal",
            # Missing required fields: target, platform
        }

        with self.assertRaises(ValidationError) as context:
            validator.validate_yaml_data(invalid_data, 'check', '/test/file.yaml')

        error_message = str(context.exception)
        self.assertIn("Validation failed for file: /test/file.yaml", error_message)
        self.assertIn("Schema: check", error_message)

    def test_invalid_yaml_data_wrong_type(self):
        """Test validation with wrong data types"""
        validator = YamlValidator(self.temp_dir)

        invalid_data = {
            "id": "0001",
            "check": {
                "ja": "日本語のチェック内容",
                "en": "English check content"
            },
            "severity": "invalid_severity",  # Invalid enum value
            "target": "design",
            "platform": ["web", "mobile"]
        }

        with self.assertRaises(ValidationError) as context:
            validator.validate_yaml_data(invalid_data, 'check', '/test/file.yaml')

        error_message = str(context.exception)
        self.assertIn("'invalid_severity' is not one of", error_message)

    def test_invalid_yaml_data_ref_validation(self):
        """Test validation with $ref that fails"""
        validator = YamlValidator(self.temp_dir)

        invalid_data = {
            "id": "0001",
            "check": {
                "ja": "日本語のチェック内容"
                # Missing required "en" field in i18nString
            },
            "severity": "normal",
            "target": "design",
            "platform": ["web", "mobile"]
        }

        with self.assertRaises(ValidationError) as context:
            validator.validate_yaml_data(invalid_data, 'check', '/test/file.yaml')

        error_message = str(context.exception)
        self.assertIn("'en' is a required property", error_message)

    def test_unknown_schema(self):
        """Test validation with unknown schema name"""
        validator = YamlValidator(self.temp_dir)

        valid_data = {"test": "data"}

        with self.assertRaises(ValidationError) as context:
            validator.validate_yaml_data(valid_data, 'unknown_schema', '/test/file.yaml')

        error_message = str(context.exception)
        self.assertIn("Schema 'unknown_schema' not found", error_message)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stderr')
    def test_missing_schema_file_warning(self, mock_stderr, mock_open_func):
        """Test warning when schema file is missing"""
        # This should not raise an exception, just print a warning
        validator = YamlValidator('/nonexistent/path')

        # Validator should still be created but with empty schemas
        self.assertEqual(len(validator.schemas), 0)

    @patch('builtins.open', mock_open(read_data='invalid json'))
    @patch('sys.stderr')
    def test_invalid_json_schema_file(self, mock_stderr):
        """Test error handling for invalid JSON in schema file"""
        with self.assertRaises(SystemExit):
            YamlValidator('/test/path')


if __name__ == '__main__':
    unittest.main()
