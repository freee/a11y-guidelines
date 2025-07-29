"""Tests for template_manager.py module."""
import pytest
from unittest.mock import patch, Mock, mock_open
import os
import sys

from yaml2rst.template_manager import TemplateManager

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


class TestTemplateManager:
    """Test TemplateManager class functionality."""

    def test_init(self):
        """Test TemplateManager initialization."""
        template_dir = "/test/templates"

        with patch('yaml2rst.template_manager.Environment') as \
             mock_env_class, \
             patch('yaml2rst.template_manager.FileSystemLoader') as \
             mock_loader_class:

            mock_loader = Mock()
            mock_env = Mock()
            mock_env.filters = {}  # Make filters a dict-like object
            mock_loader_class.return_value = mock_loader
            mock_env_class.return_value = mock_env

            manager = TemplateManager(template_dir)

            # Verify FileSystemLoader was created with correct directory
            mock_loader_class.assert_called_once_with(template_dir)

            # Verify Environment was created with the loader
            mock_env_class.assert_called_once_with(loader=mock_loader)

            # Verify filter was registered
            assert mock_env.filters['make_heading'] == manager.make_heading

            # Verify initial state
            assert manager.template is None

    def test_load(self):
        """Test template loading."""
        template_dir = "/test/templates"
        filename = "test_template.rst"

        with patch('yaml2rst.template_manager.Environment') as \
             mock_env_class, \
             patch('yaml2rst.template_manager.FileSystemLoader'):

            mock_env = Mock()
            mock_env.filters = {}  # Make filters a dict-like object
            mock_template = Mock()
            mock_env.get_template.return_value = mock_template
            mock_env_class.return_value = mock_env

            manager = TemplateManager(template_dir)
            result = manager.load(filename)

            # Verify get_template was called with correct filename
            mock_env.get_template.assert_called_once_with(filename)

            # Verify template was stored
            assert manager.template == mock_template

            # Verify method returns self for chaining
            assert result == manager

    def test_write_rst(self):
        """Test RST file writing."""
        template_dir = "/test/templates"
        data = {"title": "Test Title", "content": "Test content"}
        output_path = "/test/output.rst"
        rendered_content = "# Test Title\nTest content"

        with patch('yaml2rst.template_manager.Environment'), \
             patch('yaml2rst.template_manager.FileSystemLoader'), \
             patch('builtins.open', mock_open()) as mock_file:

            manager = TemplateManager(template_dir)

            # Setup mock template
            mock_template = Mock()
            mock_template.render.return_value = rendered_content
            manager.template = mock_template

            manager.write_rst(data, output_path)

            # Verify template.render was called with data
            mock_template.render.assert_called_once_with(data)

            # Verify file was opened correctly
            mock_file.assert_called_once_with(
                output_path, mode='w', encoding='utf-8', newline='\n')

            # Verify content was written
            mock_file().write.assert_called_once_with(rendered_content)

    def test_make_heading_level_1_with_overline(self):
        """Test heading generation for level 1 (with overline)."""
        title = "Test Heading"
        level = 1

        result = TemplateManager.make_heading(title, level)

        expected = "############\nTest Heading\n############"
        assert result == expected

    def test_make_heading_level_2_with_overline(self):
        """Test heading generation for level 2 (with overline)."""
        title = "Test Heading"
        level = 2

        result = TemplateManager.make_heading(title, level)

        expected = "************\nTest Heading\n************"
        assert result == expected

    def test_make_heading_level_3_without_overline(self):
        """Test heading generation for level 3 (without overline)."""
        title = "Test Heading"
        level = 3

        result = TemplateManager.make_heading(title, level)

        expected = "Test Heading\n============"
        assert result == expected

    def test_make_heading_level_4_without_overline(self):
        """Test heading generation for level 4 (without overline)."""
        title = "Test Heading"
        level = 4

        result = TemplateManager.make_heading(title, level)

        expected = "Test Heading\n------------"
        assert result == expected

    def test_make_heading_level_5_without_overline(self):
        """Test heading generation for level 5 (without overline)."""
        title = "Test Heading"
        level = 5

        result = TemplateManager.make_heading(title, level)

        expected = "Test Heading\n^^^^^^^^^^^^"
        assert result == expected

    def test_make_heading_level_6_without_overline(self):
        """Test heading generation for level 6 (without overline)."""
        title = "Test Heading"
        level = 6

        result = TemplateManager.make_heading(title, level)

        expected = 'Test Heading\n""""""""""""'
        assert result == expected

    def test_make_heading_with_class_name(self):
        """Test heading generation with CSS class name."""
        title = "Test Heading"
        level = 3
        class_name = "custom-class"

        result = TemplateManager.make_heading(title, level, class_name)

        expected = (".. rst-class:: custom-class\n\n"
                    "Test Heading\n============")
        assert result == expected

    def test_make_heading_with_class_name_and_overline(self):
        """Test heading generation with CSS class name and overline."""
        title = "Test Heading"
        level = 1
        class_name = "main-title"

        result = TemplateManager.make_heading(title, level, class_name)

        expected = (".. rst-class:: main-title\n\n"
                    "############\nTest Heading\n############")
        assert result == expected

    def test_make_heading_multibyte_characters(self):
        """Test heading generation with multibyte characters."""
        title = "テストヘッダー"  # Japanese characters
        level = 3

        result = TemplateManager.make_heading(title, level)

        # Each Japanese character should be counted as width 2
        # "テストヘッダー" = 7 characters × 2 = 14 width
        expected = "テストヘッダー\n=============="
        assert result == expected

    def test_make_heading_mixed_characters(self):
        """Test heading generation with mixed ASCII and multibyte
        characters."""
        title = "Test テスト"  # Mixed English and Japanese
        level = 3

        result = TemplateManager.make_heading(title, level)

        # "Test " = 5 ASCII chars (width 5) + "テスト" = 3 Japanese chars
        # (width 6) = total width 11
        expected = "Test テスト\n==========="
        assert result == expected

    def test_make_heading_invalid_level_too_low(self):
        """Test heading generation with invalid level (too low)."""
        title = "Test Heading"
        level = 0

        with pytest.raises(ValueError,
                           match="Invalid level: 0. Must be between 1 and 6"):
            TemplateManager.make_heading(title, level)

    def test_make_heading_invalid_level_too_high(self):
        """Test heading generation with invalid level (too high)."""
        title = "Test Heading"
        level = 7

        with pytest.raises(ValueError,
                           match="Invalid level: 7. Must be between 1 and 6"):
            TemplateManager.make_heading(title, level)

    def test_make_heading_empty_title(self):
        """Test heading generation with empty title."""
        title = ""
        level = 3

        result = TemplateManager.make_heading(title, level)

        expected = "\n"
        assert result == expected

    def test_make_heading_single_character(self):
        """Test heading generation with single character title."""
        title = "A"
        level = 3

        result = TemplateManager.make_heading(title, level)

        expected = "A\n="
        assert result == expected

    def test_width_calculation_ascii(self):
        """Test width calculation for ASCII characters."""
        # Access the internal width function through make_heading
        title = "Hello"
        level = 3

        result = TemplateManager.make_heading(title, level)

        # "Hello" should have width 5
        expected = "Hello\n====="
        assert result == expected

    def test_width_calculation_fullwidth(self):
        """Test width calculation for fullwidth characters."""
        title = "Ａ"  # Fullwidth A
        level = 3

        result = TemplateManager.make_heading(title, level)

        # Fullwidth A should have width 2
        expected = "Ａ\n=="
        assert result == expected

    def test_width_calculation_wide_characters(self):
        """Test width calculation for wide characters."""
        title = "한글"  # Korean characters
        level = 3

        result = TemplateManager.make_heading(title, level)

        # Korean characters should have width 2 each
        expected = "한글\n===="
        assert result == expected

    def test_integration_load_and_write(self):
        """Test integration of load and write_rst methods."""
        template_dir = "/test/templates"
        filename = "test.rst"
        data = {"title": "Integration Test"}
        output_path = "/test/output.rst"
        rendered_content = "Integration Test Content"

        with patch('yaml2rst.template_manager.Environment') as \
             mock_env_class, \
             patch('yaml2rst.template_manager.FileSystemLoader'), \
             patch('builtins.open', mock_open()) as mock_file:

            mock_env = Mock()
            mock_env.filters = {}  # Make filters a dict-like object
            mock_template = Mock()
            mock_template.render.return_value = rendered_content
            mock_env.get_template.return_value = mock_template
            mock_env_class.return_value = mock_env

            manager = TemplateManager(template_dir)

            # Chain load and write_rst
            manager.load(filename).write_rst(data, output_path)

            # Verify the chain worked
            mock_env.get_template.assert_called_once_with(filename)
            mock_template.render.assert_called_once_with(data)
            mock_file().write.assert_called_once_with(rendered_content)
