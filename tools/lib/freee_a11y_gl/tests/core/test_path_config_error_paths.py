"""Tests for path_config.py error handling paths."""
from unittest.mock import patch

import pytest

from freee_a11y_gl.config.path_config import PathConfig


class TestPathConfigErrorPaths:
    """Test error handling paths in PathConfig."""

    @patch('freee_a11y_gl.config.path_config.settings')
    def test_get_base_url_exception_fallback(self, mock_settings):
        """Test get_base_url falls back when exception occurs."""
        # Mock settings to raise an exception
        mock_settings.get.side_effect = Exception("Settings error")
        
        result = PathConfig.get_base_url("ja")
        
        # Should fallback to empty string
        assert result == ""

    @patch('freee_a11y_gl.config.path_config.settings')
    def test_get_examples_url_exception_fallback(self, mock_settings):
        """Test get_examples_url falls back when exception occurs."""
        # Mock PathConfig.get_base_url to raise an exception
        with patch.object(PathConfig, 'get_base_url', side_effect=Exception("Base URL error")):
            result = PathConfig.get_examples_url("ja")
            
            # Should fallback to relative path
            assert result == "/checks/examples/"

    def test_none_language_code_in_get_base_url(self):
        """Test get_base_url with None language code."""
        # This should work without errors
        result = PathConfig.get_base_url(None)
        
        # Should still return a string
        assert isinstance(result, str)

    def test_none_language_code_in_get_examples_url(self):
        """Test get_examples_url with None language code."""
        # This should work without errors
        result = PathConfig.get_examples_url(None)
        
        # Should still return a string
        assert isinstance(result, str)