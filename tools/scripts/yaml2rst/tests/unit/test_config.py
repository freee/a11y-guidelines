"""Tests for config.py module."""
from unittest.mock import patch
import sys
import os

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


class TestConfig:
    """Test configuration functionality."""

    @patch('yaml2rst.config.Config.get_available_languages')
    def test_get_available_languages_success(self, mock_config_method):
        """Test successful retrieval of available languages."""
        # Setup mock to return expected languages
        mock_config_method.return_value = ['ja', 'en', 'fr']

        from yaml2rst.config import get_available_languages

        result = get_available_languages()

        assert result == ['ja', 'en', 'fr']
        mock_config_method.assert_called_once()

    @patch('yaml2rst.config.Config.get_available_languages')
    def test_get_available_languages_exception_fallback(self,
                                                        mock_config_method):
        """Test fallback behavior when Config raises an exception."""
        # Setup mock to raise an exception
        mock_config_method.side_effect = Exception("Settings not initialized")

        from yaml2rst.config import get_available_languages

        result = get_available_languages()

        # Should return fallback languages
        assert result == ["ja", "en"]
        mock_config_method.assert_called_once()

    @patch('yaml2rst.config.Config.get_available_languages')
    def test_get_available_languages_attribute_error_fallback(
            self, mock_config_method):
        """Test fallback behavior when Config doesn't have the method."""
        # Setup mock to raise AttributeError
        mock_config_method.side_effect = AttributeError(
            "'Config' object has no attribute 'get_available_languages'")

        from yaml2rst.config import get_available_languages

        result = get_available_languages()

        # Should return fallback languages
        assert result == ["ja", "en"]
        mock_config_method.assert_called_once()

    @patch('yaml2rst.config.Config')
    def test_get_available_languages_import_error_fallback(
            self, mock_config_class):
        """Test fallback behavior when Config import fails."""
        # Setup mock to raise ImportError when accessing languages
        mock_config_class.get_available_languages.side_effect = (
            ImportError("Cannot import Config"))

        from yaml2rst.config import get_available_languages

        result = get_available_languages()

        # Should return fallback languages
        assert result == ["ja", "en"]

    def test_available_languages_constant(self):
        """Test that AVAILABLE_LANGUAGES constant is properly set."""
        from yaml2rst.config import AVAILABLE_LANGUAGES

        # Should be a list
        assert isinstance(AVAILABLE_LANGUAGES, list)

        # Should contain at least the fallback languages
        assert 'ja' in AVAILABLE_LANGUAGES
        assert 'en' in AVAILABLE_LANGUAGES

    def test_available_languages_constant_initialization(self):
        """Test that AVAILABLE_LANGUAGES is initialized properly."""
        # This test verifies that the constant is properly initialized
        # We don't need to mock since we're testing actual initialization
        from yaml2rst.config import (AVAILABLE_LANGUAGES,
                                     get_available_languages)

        # The constant should match what get_available_languages returns
        expected_languages = get_available_languages()
        assert AVAILABLE_LANGUAGES == expected_languages

        # Should contain at least the fallback languages
        assert 'ja' in AVAILABLE_LANGUAGES
        assert 'en' in AVAILABLE_LANGUAGES

    def test_module_structure(self):
        """Test the overall structure of the config module."""
        import yaml2rst.config

        # Verify expected functions and constants exist
        assert hasattr(yaml2rst.config, 'get_available_languages')
        assert hasattr(yaml2rst.config, 'AVAILABLE_LANGUAGES')
        assert callable(yaml2rst.config.get_available_languages)

    def test_backward_compatibility(self):
        """Test that the module maintains backward compatibility."""
        from yaml2rst.config import (AVAILABLE_LANGUAGES,
                                     get_available_languages)

        # Both should return the same languages
        constant_languages = AVAILABLE_LANGUAGES
        function_languages = get_available_languages()

        # They should be equivalent (not necessarily the same object)
        assert set(constant_languages) == set(function_languages)
