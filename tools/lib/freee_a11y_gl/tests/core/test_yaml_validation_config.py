"""
Tests for YAML validation configuration functionality.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from freee_a11y_gl.config import Config
from freee_a11y_gl.yaml_validator import YamlValidator
from freee_a11y_gl.yaml_validator import ValidationError as YamlValidationError
from freee_a11y_gl.exceptions import ValidationError
from freee_a11y_gl.settings import settings


class TestYamlValidationConfig:
    """Test YAML validation configuration functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Reset settings to default state
        settings._settings = {
            "languages": {
                "available": ["ja", "en"],
                "default": "ja"
            },
            "base_url": "https://a11y-guidelines.freee.co.jp",
            "paths": {
                "guidelines": "/categories/",
                "faq": "/faq/articles/"
            },
            "validation": {
                "yaml_validation": "strict"
            },
            "axe_core": {
                "submodule_name": "vendor/axe-core",
                "base_dir": "vendor/axe-core",
                "deque_url": "https://dequeuniversity.com/rules/axe/",
                "pkg_file": "package.json",
                "rules_dir": "lib/rules",
                "locale_dir": "locales",
                "locale_ja_file": "ja.json"
            }
        }
        settings.validate()

    def test_default_validation_mode(self):
        """Test that default validation mode is 'strict'."""
        mode = Config.get_yaml_validation_mode()
        assert mode == "strict"

    def test_set_validation_mode_valid(self):
        """Test setting valid validation modes."""
        valid_modes = ["strict", "warning", "disabled"]

        for mode in valid_modes:
            Config.set_yaml_validation_mode(mode)
            assert Config.get_yaml_validation_mode() == mode

    def test_set_validation_mode_invalid(self):
        """Test setting invalid validation mode raises ValidationError."""
        with pytest.raises(ValidationError, match="validation mode must be one of"):
            Config.set_yaml_validation_mode("invalid_mode")

    def test_config_initialize_with_validation_override(self):
        """Test initializing config with validation override."""
        Config.initialize(
            config_override={
                "validation": {
                    "yaml_validation": "warning"
                }
            }
        )

        assert Config.get_yaml_validation_mode() == "warning"

    def test_yaml_validator_initialization_with_mode(self):
        """Test YamlValidator initialization with different modes."""
        # Mock schema directory to avoid file system dependencies
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator_strict = YamlValidator("/mock/schema", "strict")
            assert validator_strict.validation_mode == "strict"

            validator_warning = YamlValidator("/mock/schema", "warning")
            assert validator_warning.validation_mode == "warning"

            validator_disabled = YamlValidator("/mock/schema", "disabled")
            assert validator_disabled.validation_mode == "disabled"

    def test_validate_with_mode_disabled(self):
        """Test validation with disabled mode."""
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator = YamlValidator("/mock/schema", "disabled")

            # Should return True without performing validation
            result = validator.validate_with_mode({}, "test_schema", "/mock/file.yaml")
            assert result is True

    def test_validate_with_mode_strict_success(self):
        """Test validation with strict mode - success case."""
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator = YamlValidator("/mock/schema", "strict")

            # Mock successful validation
            with patch.object(validator, 'validate_yaml_data') as mock_validate:
                mock_validate.return_value = None  # No exception means success

                result = validator.validate_with_mode({}, "test_schema", "/mock/file.yaml")
                assert result is True
                mock_validate.assert_called_once_with({}, "test_schema", "/mock/file.yaml")

    def test_validate_with_mode_strict_failure(self):
        """Test validation with strict mode - failure case."""
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator = YamlValidator("/mock/schema", "strict")

            # Mock validation failure
            with patch.object(validator, 'validate_yaml_data') as mock_validate:
                mock_validate.side_effect = YamlValidationError("Test validation error")

                with pytest.raises(YamlValidationError, match="Test validation error"):
                    validator.validate_with_mode({}, "test_schema", "/mock/file.yaml")

    def test_validate_with_mode_warning_success(self):
        """Test validation with warning mode - success case."""
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator = YamlValidator("/mock/schema", "warning")

            # Mock successful validation
            with patch.object(validator, 'validate_yaml_data') as mock_validate:
                mock_validate.return_value = None  # No exception means success

                result = validator.validate_with_mode({}, "test_schema", "/mock/file.yaml")
                assert result is True

    def test_validate_with_mode_warning_failure(self):
        """Test validation with warning mode - failure case."""
        with patch('os.path.join'), \
             patch('builtins.open'), \
             patch('json.load'), \
             patch('os.path.abspath'):

            validator = YamlValidator("/mock/schema", "warning")

            # Mock validation failure
            with patch.object(validator, 'validate_yaml_data') as mock_validate:
                mock_validate.side_effect = YamlValidationError("Test validation error")

                with patch('builtins.print') as mock_print:
                    result = validator.validate_with_mode({}, "test_schema", "/mock/file.yaml")

                    # Should return False and print warning
                    assert result is False
                    mock_print.assert_called_once()
                    args, kwargs = mock_print.call_args
                    assert "YAML Validation Warning" in args[0]
                    assert kwargs.get('file') == sys.stderr

    def test_integration_with_initializer_config(self):
        """Test integration with initializer configuration."""
        # Set validation mode to disabled
        Config.set_yaml_validation_mode("disabled")

        # Mock all the dependencies to avoid file system operations
        with patch('freee_a11y_gl.initializer.get_src_path') as mock_get_src_path, \
             patch('freee_a11y_gl.initializer.process_static_entity_file'), \
             patch('freee_a11y_gl.initializer.process_entity_files'), \
             patch('freee_a11y_gl.initializer.process_axe_rules'), \
             patch('freee_a11y_gl.initializer.RelationshipManager') as mock_rel_manager, \
             patch('freee_a11y_gl.initializer.CheckTool'), \
             patch('freee_a11y_gl.initializer.YamlValidator') as mock_validator_class:

            mock_get_src_path.return_value = {
                'checks': '/mock/checks',
                'guidelines': '/mock/guidelines',
                'faq': '/mock/faq',
                'gl_categories': '/mock/categories.json',
                'wcag_sc': '/mock/wcag.json',
                'faq_tags': '/mock/tags.json',
                'info': '/mock/info.json'
            }
            mock_rel_manager.return_value.resolve_faqs.return_value = None

            # Import and call setup_instances
            from freee_a11y_gl.initializer import setup_instances
            setup_instances('/mock/basedir')

            # Verify YamlValidator was initialized with disabled mode
            # The call should include the schema directory path and validation mode
            mock_validator_class.assert_called_once()
            call_args = mock_validator_class.call_args
            assert call_args[0][1] == 'disabled'  # Second argument should be validation mode

    def test_backward_compatibility(self):
        """Test that existing code continues to work without configuration changes."""
        # Test that validate_yaml_data method still works as before
        with patch('freee_a11y_gl.yaml_validator.os.path.join'), \
             patch('builtins.open'), \
             patch('freee_a11y_gl.yaml_validator.json.load'), \
             patch('freee_a11y_gl.yaml_validator.os.path.abspath'):

            validator = YamlValidator("/mock/schema")  # Default mode should be strict
            assert validator.validation_mode == "strict"

            # The original validate_yaml_data method should still work
            with patch.object(validator, 'schemas', {'test': {}}), \
                 patch.object(validator, 'resolvers', {'test': MagicMock()}), \
                 patch('freee_a11y_gl.yaml_validator.Draft202012Validator') as mock_validator_class:

                mock_validator_instance = MagicMock()
                mock_validator_class.return_value = mock_validator_instance
                mock_validator_instance.iter_errors.return_value = []  # No errors

                # Should not raise exception
                validator.validate_yaml_data({}, "test", "/mock/file.yaml")

                # Verify validator was called
                mock_validator_class.assert_called_once()
                mock_validator_instance.iter_errors.assert_called_once_with({})

    def test_settings_validation_config_structure(self):
        """Test that settings properly validate ValidationConfig structure."""
        from freee_a11y_gl.settings import ValidationConfig

        # Test valid configurations
        valid_config = ValidationConfig(yaml_validation="strict")
        assert valid_config.yaml_validation == "strict"

        valid_config = ValidationConfig(yaml_validation="warning")
        assert valid_config.yaml_validation == "warning"

        valid_config = ValidationConfig(yaml_validation="disabled")
        assert valid_config.yaml_validation == "disabled"

        # Test default value
        default_config = ValidationConfig()
        assert default_config.yaml_validation == "strict"

    def test_settings_global_config_with_validation(self):
        """Test that GlobalConfig properly includes ValidationConfig."""
        from freee_a11y_gl.settings import GlobalConfig, LanguageConfig, PathConfig, ValidationConfig, AxeCoreConfig

        axe_core_config = AxeCoreConfig(
            submodule_name="vendor/axe-core",
            base_dir="vendor/axe-core",
            deque_url="https://dequeuniversity.com/rules/axe/",
            pkg_file="package.json",
            rules_dir="lib/rules",
            locale_dir="locales",
            locale_ja_file="ja.json"
        )

        config = GlobalConfig(
            languages=LanguageConfig(available=["ja", "en"], default="ja"),
            base_url="https://example.com",
            paths=PathConfig(guidelines="/categories/", faq="/faq/"),
            validation=ValidationConfig(yaml_validation="warning"),
            axe_core=axe_core_config
        )

        assert config.validation.yaml_validation == "warning"

        # Test with default validation config
        config_default = GlobalConfig(
            languages=LanguageConfig(available=["ja", "en"], default="ja"),
            base_url="https://example.com",
            paths=PathConfig(guidelines="/categories/", faq="/faq/"),
            axe_core=axe_core_config
        )

        assert config_default.validation.yaml_validation == "strict"
