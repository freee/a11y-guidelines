"""
Comprehensive tests for settings module.
"""

import json
import os
import tempfile
import unittest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from pydantic import ValidationError

from freee_a11y_gl.settings import (
    Settings,
    LanguageConfig,
    PathConfig,
    ValidationConfig,
    GlobalConfig,
    settings
)


class TestLanguageConfig(unittest.TestCase):
    """Test cases for LanguageConfig model"""

    def test_language_config_creation(self):
        """Test LanguageConfig creation with valid data"""
        config = LanguageConfig(available=["ja", "en"], default="ja")
        self.assertEqual(config.available, ["ja", "en"])
        self.assertEqual(config.default, "ja")

    def test_language_config_validation(self):
        """Test LanguageConfig validation"""
        # Valid configuration
        config = LanguageConfig(available=["ja", "en", "fr"], default="en")
        self.assertEqual(len(config.available), 3)
        self.assertEqual(config.default, "en")


class TestPathConfig(unittest.TestCase):
    """Test cases for PathConfig model"""

    def test_path_config_valid_paths(self):
        """Test PathConfig with valid paths"""
        config = PathConfig(guidelines="/categories/", faq="/faq/articles/")
        self.assertEqual(config.guidelines, "/categories/")
        self.assertEqual(config.faq, "/faq/articles/")

    def test_path_config_invalid_paths(self):
        """Test PathConfig with invalid paths"""
        # Path not starting with /
        with self.assertRaises(ValidationError):
            PathConfig(guidelines="categories/", faq="/faq/articles/")
        
        # Path not ending with /
        with self.assertRaises(ValidationError):
            PathConfig(guidelines="/categories", faq="/faq/articles/")
        
        # Empty path
        with self.assertRaises(ValidationError):
            PathConfig(guidelines="", faq="/faq/articles/")

    def test_path_config_edge_cases(self):
        """Test PathConfig edge cases"""
        # Minimal valid paths
        config = PathConfig(guidelines="/", faq="/")
        self.assertEqual(config.guidelines, "/")
        self.assertEqual(config.faq, "/")


class TestValidationConfig(unittest.TestCase):
    """Test cases for ValidationConfig model"""

    def test_validation_config_default(self):
        """Test ValidationConfig default value"""
        config = ValidationConfig()
        self.assertEqual(config.yaml_validation, "strict")

    def test_validation_config_valid_modes(self):
        """Test ValidationConfig with valid modes"""
        for mode in ["strict", "warning", "disabled"]:
            config = ValidationConfig(yaml_validation=mode)
            self.assertEqual(config.yaml_validation, mode)

    def test_validation_config_invalid_mode(self):
        """Test ValidationConfig with invalid mode"""
        with self.assertRaises(ValidationError):
            ValidationConfig(yaml_validation="invalid_mode")


class TestGlobalConfig(unittest.TestCase):
    """Test cases for GlobalConfig model"""

    def test_global_config_creation(self):
        """Test GlobalConfig creation with valid data"""
        config_data = {
            "languages": {"available": ["ja", "en"], "default": "ja"},
            "base_url": "https://example.com",
            "paths": {"guidelines": "/categories/", "faq": "/faq/articles/"},
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
        config = GlobalConfig(**config_data)
        
        self.assertEqual(config.languages.available, ["ja", "en"])
        self.assertEqual(config.languages.default, "ja")
        self.assertEqual(config.base_url, "https://example.com")
        self.assertEqual(config.paths.guidelines, "/categories/")
        self.assertEqual(config.paths.faq, "/faq/articles/")
        self.assertEqual(config.validation.yaml_validation, "strict")  # Default

    def test_global_config_with_validation(self):
        """Test GlobalConfig with validation settings"""
        config_data = {
            "languages": {"available": ["ja", "en"], "default": "ja"},
            "base_url": "https://example.com",
            "paths": {"guidelines": "/categories/", "faq": "/faq/articles/"},
            "validation": {"yaml_validation": "warning"},
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
        config = GlobalConfig(**config_data)
        self.assertEqual(config.validation.yaml_validation, "warning")


class TestSettings(unittest.TestCase):
    """Test cases for Settings class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".config" / "freee_a11y_gl"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_settings_initialization_default(self):
        """Test Settings initialization with defaults"""
        with patch.object(Settings, 'load_defaults'), \
             patch.object(Settings, 'load_from_profile'), \
             patch.object(Settings, 'load_message_catalog'), \
             patch.object(Settings, 'validate'):
            
            settings_instance = Settings()
            self.assertEqual(settings_instance._profile, "default")

    def test_settings_initialization_with_profile(self):
        """Test Settings initialization with custom profile"""
        with patch.object(Settings, 'load_defaults'), \
             patch.object(Settings, 'load_from_profile'), \
             patch.object(Settings, 'load_message_catalog'), \
             patch.object(Settings, 'validate'):
            
            settings_instance = Settings(profile="test")
            self.assertEqual(settings_instance._profile, "test")

    @patch('freee_a11y_gl.settings.resources')
    def test_load_defaults_success(self, mock_resources):
        """Test load_defaults with successful resource loading"""
        mock_config_data = {
            "languages": {"available": ["ja", "en"], "default": "ja"},
            "base_url": "https://example.com",
            "paths": {"guidelines": "/categories/", "faq": "/faq/articles/"}
        }
        
        mock_files = MagicMock()
        mock_config_file = MagicMock()
        mock_config_file.is_file.return_value = True
        mock_config_file.read_text.return_value = yaml.dump(mock_config_data)
        mock_files.__truediv__.return_value = mock_config_file
        mock_resources.files.return_value = mock_files
        
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        settings_instance.load_defaults()
        
        self.assertEqual(settings_instance._settings, mock_config_data)

    @patch('freee_a11y_gl.settings.resources')
    def test_load_defaults_file_not_found(self, mock_resources):
        """Test load_defaults when resource file not found"""
        mock_files = MagicMock()
        mock_config_file = MagicMock()
        mock_config_file.is_file.return_value = False
        mock_files.__truediv__.return_value = mock_config_file
        mock_resources.files.return_value = mock_files
        
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        settings_instance.load_defaults()
        
        # Should fall back to minimal defaults
        self.assertIn("languages", settings_instance._settings)
        self.assertEqual(settings_instance._settings["languages"]["default"], "ja")

    @patch('freee_a11y_gl.settings.resources')
    def test_load_defaults_empty_config_file(self, mock_resources):
        """Test load_defaults with empty config file"""
        mock_files = MagicMock()
        mock_config_file = MagicMock()
        mock_config_file.is_file.return_value = True
        mock_config_file.read_text.return_value = ""  # Empty file
        mock_files.__truediv__.return_value = mock_config_file
        mock_resources.files.return_value = mock_files
        
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        settings_instance.load_defaults()
        
        # Should fall back to minimal defaults
        self.assertIn("languages", settings_instance._settings)
        self.assertEqual(settings_instance._settings["languages"]["default"], "ja")

    def test_load_defaults_fallback_to_file_system(self):
        """Test load_defaults fallback to file system"""
        with patch('freee_a11y_gl.settings.resources') as mock_resources:
            mock_resources.files.side_effect = ModuleNotFoundError()
            
            # Create a mock config file
            mock_config_data = {
                "languages": {"available": ["ja", "en"], "default": "ja"},
                "base_url": "https://example.com",
                "paths": {"guidelines": "/categories/", "faq": "/faq/articles/"}
            }
            
            with patch('pathlib.Path.exists', return_value=True), \
                 patch('pathlib.Path.open', mock_open(read_data=yaml.dump(mock_config_data))):
                
                settings_instance = Settings.__new__(Settings)
                settings_instance._settings = {}
                settings_instance.load_defaults()
                
                self.assertEqual(settings_instance._settings, mock_config_data)

    def test_load_defaults_all_fallbacks_fail(self):
        """Test load_defaults when all fallbacks fail"""
        with patch('freee_a11y_gl.settings.resources') as mock_resources:
            mock_resources.files.side_effect = ModuleNotFoundError()
            
            with patch('pathlib.Path.exists', return_value=False):
                settings_instance = Settings.__new__(Settings)
                settings_instance._settings = {}
                settings_instance.load_defaults()
                
                # Should use minimal defaults
                expected_defaults = settings_instance._get_minimal_defaults()
                self.assertEqual(settings_instance._settings, expected_defaults)

    def test_get_minimal_defaults(self):
        """Test _get_minimal_defaults method"""
        settings_instance = Settings.__new__(Settings)
        defaults = settings_instance._get_minimal_defaults()
        
        self.assertIn("languages", defaults)
        self.assertIn("base_url", defaults)
        self.assertIn("paths", defaults)
        self.assertIn("validation", defaults)
        
        self.assertEqual(defaults["languages"]["default"], "ja")
        self.assertEqual(defaults["validation"]["yaml_validation"], "strict")

    @patch('pathlib.Path.home')
    def test_get_config_base_dir(self, mock_home):
        """Test _get_config_base_dir method"""
        mock_home.return_value = Path("/home/user")
        
        settings_instance = Settings.__new__(Settings)
        base_dir = settings_instance._get_config_base_dir()
        
        expected = Path("/home/user") / ".config" / "freee_a11y_gl"
        self.assertEqual(base_dir, expected)

    def test_get_profile_config_paths_default_profile(self):
        """Test _get_profile_config_paths with default profile"""
        with patch.object(Settings, '_get_config_base_dir') as mock_base_dir:
            mock_base_dir.return_value = Path("/config")
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._profile = "default"
            paths = settings_instance._get_profile_config_paths()
            
            expected_paths = [
                Path("/config/profiles/default.yaml"),
                Path("/config/lib/config.yaml")
            ]
            self.assertEqual(paths, expected_paths)

    def test_get_profile_config_paths_custom_profile(self):
        """Test _get_profile_config_paths with custom profile"""
        with patch.object(Settings, '_get_config_base_dir') as mock_base_dir:
            mock_base_dir.return_value = Path("/config")
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._profile = "custom"
            paths = settings_instance._get_profile_config_paths()
            
            expected_paths = [
                Path("/config/profiles/custom.yaml"),
                Path("/config/profiles/default.yaml"),
                Path("/config/lib/config.yaml")
            ]
            self.assertEqual(paths, expected_paths)

    def test_load_from_profile_success(self):
        """Test load_from_profile with successful file loading"""
        profile_config = {"base_url": "https://custom.example.com"}
        
        with patch.object(Settings, '_get_profile_config_paths') as mock_paths, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.open', mock_open(read_data=yaml.dump(profile_config))):
            
            mock_paths.return_value = [Path("/config/profiles/test.yaml")]
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._settings = {"base_url": "https://default.com"}
            settings_instance.update = MagicMock()
            
            settings_instance.load_from_profile()
            
            settings_instance.update.assert_called_once_with(profile_config)

    def test_load_from_profile_file_not_found(self):
        """Test load_from_profile when files don't exist"""
        with patch.object(Settings, '_get_profile_config_paths') as mock_paths, \
             patch('pathlib.Path.exists', return_value=False):
            
            mock_paths.return_value = [Path("/config/profiles/test.yaml")]
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._settings = {"base_url": "https://default.com"}
            settings_instance.update = MagicMock()
            
            settings_instance.load_from_profile()
            
            # update should not be called
            settings_instance.update.assert_not_called()

    def test_load_from_profile_permission_error(self):
        """Test load_from_profile with permission error"""
        with patch.object(Settings, '_get_profile_config_paths') as mock_paths, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.open', side_effect=PermissionError()):
            
            mock_paths.return_value = [Path("/config/profiles/test.yaml")]
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._settings = {"base_url": "https://default.com"}
            settings_instance.update = MagicMock()
            
            settings_instance.load_from_profile()
            
            # Should not raise exception, update should not be called
            settings_instance.update.assert_not_called()

    def test_load_from_profile_yaml_error(self):
        """Test load_from_profile with YAML parsing error"""
        with patch.object(Settings, '_get_profile_config_paths') as mock_paths, \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('pathlib.Path.open', mock_open(read_data="invalid: yaml: content: [")):
            
            mock_paths.return_value = [Path("/config/profiles/test.yaml")]
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._settings = {"base_url": "https://default.com"}
            settings_instance.update = MagicMock()
            
            settings_instance.load_from_profile()
            
            # Should not raise exception, update should not be called
            settings_instance.update.assert_not_called()

    @patch('freee_a11y_gl.settings.resources')
    def test_load_message_catalog_success(self, mock_resources):
        """Test load_message_catalog with successful resource loading"""
        mock_files = MagicMock()
        mock_message_file = MagicMock()
        mock_message_file.is_file.return_value = True
        mock_files.__truediv__.return_value = mock_message_file
        mock_resources.files.return_value = mock_files
        
        with patch('freee_a11y_gl.settings.MessageCatalog') as mock_catalog_class:
            mock_catalog = MagicMock()
            mock_catalog_class.load_with_fallback.return_value = mock_catalog
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._profile = "default"
            settings_instance.load_message_catalog()
            
            self.assertEqual(settings_instance._message_catalog, mock_catalog)

    def test_load_message_catalog_all_fail(self):
        """Test load_message_catalog when all attempts fail"""
        with patch.object(Settings, '_get_config_base_dir') as mock_base_dir, \
             patch('freee_a11y_gl.settings.MessageCatalog') as mock_catalog_class:
            
            mock_base_dir.return_value = Path("/config")
            mock_catalog_class.load_with_fallback.side_effect = Exception("Load failed")
            mock_default_catalog = MagicMock()
            mock_catalog_class.return_value = mock_default_catalog
            
            settings_instance = Settings.__new__(Settings)
            settings_instance._profile = "default"
            settings_instance._message_catalog = None  # Initialize the attribute
            settings_instance.load_message_catalog()
            
            # Should fall back to default MessageCatalog
            mock_catalog_class.assert_called_with()
            self.assertEqual(settings_instance._message_catalog, mock_default_catalog)

    def test_get_simple_key(self):
        """Test get method with simple key"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"key": "value"}
        
        result = settings_instance.get("key")
        self.assertEqual(result, "value")

    def test_get_nested_key(self):
        """Test get method with nested key"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"level1": {"level2": {"key": "value"}}}
        
        result = settings_instance.get("level1.level2.key")
        self.assertEqual(result, "value")

    def test_get_missing_key_with_default(self):
        """Test get method with missing key and default value"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        
        result = settings_instance.get("missing.key", "default_value")
        self.assertEqual(result, "default_value")

    def test_get_missing_key_without_default(self):
        """Test get method with missing key without default value"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        
        result = settings_instance.get("missing.key")
        self.assertIsNone(result)

    def test_set_simple_key(self):
        """Test set method with simple key"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        settings_instance.validate = MagicMock()
        
        settings_instance.set("key", "value")
        
        self.assertEqual(settings_instance._settings["key"], "value")
        settings_instance.validate.assert_called_once()

    def test_set_nested_key(self):
        """Test set method with nested key"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        settings_instance.validate = MagicMock()
        
        settings_instance.set("level1.level2.key", "value")
        
        self.assertEqual(settings_instance._settings["level1"]["level2"]["key"], "value")
        settings_instance.validate.assert_called_once()

    def test_get_nested_existing(self):
        """Test get_nested with existing keys"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"level1": {"level2": "value"}}
        
        result = settings_instance.get_nested(["level1", "level2"])
        self.assertEqual(result, "value")

    def test_get_nested_missing(self):
        """Test get_nested with missing keys"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        
        with self.assertRaises(KeyError):
            settings_instance.get_nested(["missing", "key"])

    def test_set_nested_new_structure(self):
        """Test set_nested creating new nested structure"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {}
        
        settings_instance.set_nested(["level1", "level2", "key"], "value")
        
        self.assertEqual(settings_instance._settings["level1"]["level2"]["key"], "value")

    def test_set_nested_existing_structure(self):
        """Test set_nested with existing structure"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"level1": {"existing": "old_value"}}
        
        settings_instance.set_nested(["level1", "level2"], "new_value")
        
        self.assertEqual(settings_instance._settings["level1"]["level2"], "new_value")
        self.assertEqual(settings_instance._settings["level1"]["existing"], "old_value")

    def test_update_with_settings(self):
        """Test update method with settings dict"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"existing": "value"}
        settings_instance.validate = MagicMock()
        
        update_data = {"new_key": "new_value", "nested": {"key": "value"}}
        settings_instance.update(update_data)
        
        self.assertEqual(settings_instance._settings["new_key"], "new_value")
        self.assertEqual(settings_instance._settings["nested"]["key"], "value")
        settings_instance.validate.assert_called_once()

    def test_update_with_none(self):
        """Test update method with None"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {"existing": "value"}
        settings_instance.validate = MagicMock()
        
        settings_instance.update(None)
        
        # Settings should remain unchanged
        self.assertEqual(settings_instance._settings, {"existing": "value"})
        settings_instance.validate.assert_called_once()

    def test_update_deep_merge(self):
        """Test update method with deep merge"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {
            "level1": {
                "existing_key": "existing_value",
                "nested": {"old_key": "old_value"}
            }
        }
        settings_instance.validate = MagicMock()
        
        update_data = {
            "level1": {
                "new_key": "new_value",
                "nested": {"new_key": "new_value"}
            }
        }
        settings_instance.update(update_data)
        
        # Should preserve existing values while adding new ones
        self.assertEqual(settings_instance._settings["level1"]["existing_key"], "existing_value")
        self.assertEqual(settings_instance._settings["level1"]["new_key"], "new_value")
        self.assertEqual(settings_instance._settings["level1"]["nested"]["old_key"], "old_value")
        self.assertEqual(settings_instance._settings["level1"]["nested"]["new_key"], "new_value")

    def test_validate_success(self):
        """Test validate method with valid settings"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {
            "languages": {"available": ["ja", "en"], "default": "ja"},
            "base_url": "https://example.com",
            "paths": {"guidelines": "/categories/", "faq": "/faq/articles/"},
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
        
        settings_instance.validate()
        
        self.assertIsInstance(settings_instance._config_model, GlobalConfig)

    def test_validate_failure(self):
        """Test validate method with invalid settings"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._settings = {
            "languages": {"available": ["ja", "en"], "default": "ja"},
            "base_url": "https://example.com",
            "paths": {"guidelines": "invalid_path", "faq": "/faq/articles/"}  # Invalid path
        }
        
        with self.assertRaises(ValidationError):
            settings_instance.validate()

    def test_config_property(self):
        """Test config property"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._config_model = None
        
        # Mock validate method and set up a return value
        mock_config = MagicMock()
        with patch.object(settings_instance, 'validate') as mock_validate:
            # Set up the validate method to set the _config_model
            def set_config_model():
                settings_instance._config_model = mock_config
            mock_validate.side_effect = set_config_model
            
            # First access should trigger validation
            config = settings_instance.config
            mock_validate.assert_called_once()
            self.assertEqual(config, mock_config)
            
            # Second access should not trigger validation again
            mock_validate.reset_mock()
            config2 = settings_instance.config
            mock_validate.assert_not_called()
            
            self.assertEqual(config, config2)

    def test_message_catalog_property(self):
        """Test message_catalog property"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._message_catalog = None
        
        # Mock load_message_catalog method and set up a return value
        mock_catalog = MagicMock()
        with patch.object(settings_instance, 'load_message_catalog') as mock_load:
            # Set up the load method to set the _message_catalog
            def set_message_catalog():
                settings_instance._message_catalog = mock_catalog
            mock_load.side_effect = set_message_catalog
            
            # First access should trigger loading
            catalog = settings_instance.message_catalog
            mock_load.assert_called_once()
            self.assertEqual(catalog, mock_catalog)
            
            # Second access should not trigger loading again
            mock_load.reset_mock()
            catalog2 = settings_instance.message_catalog
            mock_load.assert_not_called()
            
            self.assertEqual(catalog, catalog2)

    def test_initialize_with_profile_change(self):
        """Test initialize method with profile change"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._profile = "old_profile"
        settings_instance.load_defaults = MagicMock()
        settings_instance.load_from_profile = MagicMock()
        settings_instance.load_message_catalog = MagicMock()
        settings_instance.update = MagicMock()
        
        settings_instance.initialize(profile="new_profile", config_override={"key": "value"})
        
        self.assertEqual(settings_instance._profile, "new_profile")
        settings_instance.load_defaults.assert_called_once()
        settings_instance.load_from_profile.assert_called_once()
        settings_instance.load_message_catalog.assert_called_once()
        settings_instance.update.assert_called_once_with({"key": "value"})

    def test_initialize_same_profile(self):
        """Test initialize method with same profile"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._profile = "test_profile"
        settings_instance.load_defaults = MagicMock()
        settings_instance.load_from_profile = MagicMock()
        settings_instance.load_message_catalog = MagicMock()
        settings_instance.update = MagicMock()
        
        settings_instance.initialize(profile="test_profile", config_override={"key": "value"})
        
        # Profile didn't change, so reload methods should not be called
        settings_instance.load_defaults.assert_not_called()
        settings_instance.load_from_profile.assert_not_called()
        settings_instance.load_message_catalog.assert_not_called()
        settings_instance.update.assert_called_once_with({"key": "value"})

    def test_initialize_no_config_override(self):
        """Test initialize method without config override"""
        settings_instance = Settings.__new__(Settings)
        settings_instance._profile = "old_profile"
        settings_instance.load_defaults = MagicMock()
        settings_instance.load_from_profile = MagicMock()
        settings_instance.load_message_catalog = MagicMock()
        settings_instance.update = MagicMock()
        
        settings_instance.initialize(profile="new_profile")
        
        self.assertEqual(settings_instance._profile, "new_profile")
        settings_instance.load_defaults.assert_called_once()
        settings_instance.load_from_profile.assert_called_once()
        settings_instance.load_message_catalog.assert_called_once()
        settings_instance.update.assert_not_called()


class TestSettingsSingleton(unittest.TestCase):
    """Test cases for settings singleton"""

    def test_settings_singleton_exists(self):
        """Test that settings singleton is available"""
        from freee_a11y_gl.settings import settings
        self.assertIsInstance(settings, Settings)

    def test_settings_singleton_properties(self):
        """Test settings singleton basic properties"""
        from freee_a11y_gl.settings import settings
        
        # Should have basic structure
        self.assertTrue(hasattr(settings, '_settings'))
        self.assertTrue(hasattr(settings, '_profile'))
        self.assertTrue(hasattr(settings, 'get'))
        self.assertTrue(hasattr(settings, 'set'))


if __name__ == '__main__':
    unittest.main()
