"""Unit tests for template export functionality."""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, call
import pytest

from yaml2rst.initializer import (
    export_templates,
    TemplateExportError,
    setup_parameters,
    parse_args
)
from yaml2rst.template_config import TemplateConfig


class TestExportTemplates:
    """Test cases for the export_templates function."""

    def test_export_templates_to_custom_directory(self, temp_dir):
        """Test exporting templates to a custom directory."""
        target_dir = temp_dir / "custom_templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin_templates"
        mock_filenames = {
            'category_page': 'gl-category.rst',
            'faq_article': 'faq/article.rst',
            'tool_example': 'checks/examples-tool.rst'
        }
        
        # Create mock source files
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("{{ category.title }}")
        (builtin_dir / "faq").mkdir(exist_ok=True)
        (builtin_dir / "faq" / "article.rst").write_text("{{ faq.title }}")
        (builtin_dir / "checks").mkdir(exist_ok=True)
        (builtin_dir / "checks" / "examples-tool.rst").write_text(
            "{{ check.title }}")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames):
            
            # Export templates
            export_templates(str(target_dir))
            
            # Verify files were copied
            assert (target_dir / "gl-category.rst").exists()
            assert (target_dir / "faq" / "article.rst").exists()
            assert (target_dir / "checks" / "examples-tool.rst").exists()
            
            # Verify content was preserved
            assert (target_dir / "gl-category.rst").read_text() == \
                   "{{ category.title }}"
            assert (target_dir / "faq" / "article.rst").read_text() == \
                   "{{ faq.title }}"

    def test_export_templates_to_default_directory(self, temp_dir):
        """Test exporting templates to default user directory."""
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin_templates"
        mock_filenames = {'category_page': 'gl-category.rst'}
        
        # Create mock source file
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("{{ category.title }}")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames), \
             patch('yaml2rst.initializer.TemplateConfig') as mock_config_class:
            
            mock_config = Mock()
            mock_config.get_user_template_dir_expanded.return_value = \
                temp_dir / "user_templates"
            mock_config_class.return_value = mock_config
            
            # Export templates (no target_dir specified)
            export_templates()
            
            # Verify template config was used
            mock_config.load_config.assert_called_once()
            mock_config.get_user_template_dir_expanded.assert_called_once()
            
            # Verify file was copied to default location
            assert (temp_dir / "user_templates" / "gl-category.rst").exists()

    def test_export_templates_creates_subdirectories(self, temp_dir):
        """Test that export creates necessary subdirectories."""
        target_dir = temp_dir / "templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {
            'faq_article': 'faq/nested/article.rst',
            'check_tool': 'checks/tools/example.rst'
        }
        
        # Create nested source files
        (builtin_dir / "faq" / "nested").mkdir(parents=True, exist_ok=True)
        (builtin_dir / "faq" / "nested" / "article.rst").write_text("test")
        (builtin_dir / "checks" / "tools").mkdir(parents=True, exist_ok=True)
        (builtin_dir / "checks" / "tools" / "example.rst").write_text("test")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames):
            
            export_templates(str(target_dir))
            
            # Verify nested directories were created
            assert (target_dir / "faq" / "nested" / "article.rst").exists()
            assert (target_dir / "checks" / "tools" / "example.rst").exists()

    def test_export_templates_missing_source_file(self, temp_dir):
        """Test error handling when source template is missing."""
        target_dir = temp_dir / "templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {'category_page': 'missing.rst'}
        
        # Don't create the source file
        builtin_dir.mkdir(parents=True, exist_ok=True)
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames):
            
            with pytest.raises(TemplateExportError, 
                             match="Built-in template not found"):
                export_templates(str(target_dir))

    def test_export_templates_permission_error(self, temp_dir):
        """Test error handling for permission errors."""
        target_dir = temp_dir / "readonly"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {'category_page': 'gl-category.rst'}
        
        # Create source file
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("test")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames), \
             patch('shutil.copy2') as mock_copy:
            
            # Mock permission error
            mock_copy.side_effect = PermissionError("Access denied")
            
            with pytest.raises(TemplateExportError, 
                             match="Permission denied when exporting templates"):
                export_templates(str(target_dir))

    def test_export_templates_os_error(self, temp_dir):
        """Test error handling for OS errors."""
        target_dir = temp_dir / "templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {'category_page': 'gl-category.rst'}
        
        # Create source file
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("test")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames), \
             patch('shutil.copy2') as mock_copy:
            
            # Mock OS error
            mock_copy.side_effect = OSError("Disk full")
            
            with pytest.raises(TemplateExportError, 
                             match="File system error during template export"):
                export_templates(str(target_dir))

    def test_export_templates_unexpected_error(self, temp_dir):
        """Test error handling for unexpected errors."""
        target_dir = temp_dir / "templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {'category_page': 'gl-category.rst'}
        
        # Create source file
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("test")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames), \
             patch('shutil.copy2') as mock_copy:
            
            # Mock unexpected error
            mock_copy.side_effect = ValueError("Unexpected error")
            
            with pytest.raises(TemplateExportError, 
                             match="Unexpected error during template export"):
                export_templates(str(target_dir))

    def test_export_templates_user_feedback(self, temp_dir, capsys):
        """Test that export provides appropriate user feedback."""
        target_dir = temp_dir / "templates"
        
        # Setup mock template directory and files
        builtin_dir = temp_dir / "builtin"
        mock_filenames = {
            'category_page': 'gl-category.rst',
            'faq_article': 'faq/article.rst'
        }
        
        # Create source files
        builtin_dir.mkdir(parents=True, exist_ok=True)
        (builtin_dir / "gl-category.rst").write_text("test")
        (builtin_dir / "faq").mkdir(exist_ok=True)
        (builtin_dir / "faq" / "article.rst").write_text("test")
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR', str(builtin_dir)), \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', mock_filenames):
            
            export_templates(str(target_dir))
            
            # Check output
            captured = capsys.readouterr()
            assert f"Templates exported to: {target_dir}" in captured.out
            assert "Exported 2 template files:" in captured.out
            assert "- faq/article.rst" in captured.out
            assert "- gl-category.rst" in captured.out
            assert "To customize templates:" in captured.out


class TestCLIIntegration:
    """Test CLI integration for template export functionality."""

    def test_parse_args_export_templates_flag(self):
        """Test that --export-templates flag is parsed correctly."""
        with patch('sys.argv', ['yaml2rst', '--export-templates']):
            args = parse_args()
            assert args.export_templates is True

    def test_parse_args_export_templates_with_template_dir(self):
        """Test --export-templates with --template-dir."""
        with patch('sys.argv', ['yaml2rst', '--export-templates', 
                                '--template-dir', '/custom/path']):
            args = parse_args()
            assert args.export_templates is True
            assert args.template_dir == '/custom/path'

    def test_setup_parameters_export_mode_exits(self, temp_dir):
        """Test that setup_parameters exits when export mode is enabled."""
        with patch('sys.argv', ['yaml2rst', '--export-templates']), \
             patch('yaml2rst.initializer.export_templates') as mock_export, \
             patch('sys.exit') as mock_exit:
            
            setup_parameters()
            
            mock_export.assert_called_once_with(None)
            mock_exit.assert_called_once_with(0)

    def test_setup_parameters_export_mode_with_custom_dir(self, temp_dir):
        """Test export mode with custom template directory."""
        custom_dir = str(temp_dir / "custom")
        
        with patch('sys.argv', ['yaml2rst', '--export-templates', 
                                '--template-dir', custom_dir]), \
             patch('yaml2rst.initializer.export_templates') as mock_export, \
             patch('sys.exit') as mock_exit:
            
            setup_parameters()
            
            mock_export.assert_called_once_with(custom_dir)
            mock_exit.assert_called_once_with(0)

    def test_setup_parameters_normal_mode_continues(self):
        """Test that normal mode continues without exiting."""
        with patch('sys.argv', ['yaml2rst', '--lang', 'ja']), \
             patch('yaml2rst.initializer.process_arguments') as mock_process:
            
            mock_process.return_value = {'lang': 'ja', 'build_all': True}
            
            result = setup_parameters()
            
            mock_process.assert_called_once()
            assert result['lang'] == 'ja'

    def test_help_message_includes_export_templates(self):
        """Test that help message includes --export-templates option."""
        with patch('sys.argv', ['yaml2rst', '--help']), \
             patch('yaml2rst.initializer.config.get_available_languages') \
             as mock_langs:
            
            mock_langs.return_value = ['ja', 'en']
            
            with pytest.raises(SystemExit) as exc_info:
                parse_args()
            
            # Help should exit with code 0
            assert exc_info.value.code == 0


class TestTemplateExportError:
    """Test the TemplateExportError exception."""

    def test_template_export_error_creation(self):
        """Test creating TemplateExportError."""
        error = TemplateExportError("Test error message")
        assert str(error) == "Test error message"

    def test_template_export_error_with_cause(self):
        """Test TemplateExportError with cause."""
        original_error = OSError("Original error")
        
        try:
            raise TemplateExportError("Wrapped error") from original_error
        except TemplateExportError as e:
            assert str(e) == "Wrapped error"
            assert e.__cause__ is original_error


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_export_templates_empty_template_filenames(self, temp_dir):
        """Test export with empty TEMPLATE_FILENAMES."""
        target_dir = temp_dir / "templates"
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR') as mock_template_dir, \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES', {}):
            
            mock_template_dir = str(temp_dir / "builtin")
            Path(mock_template_dir).mkdir(parents=True, exist_ok=True)
            
            export_templates(str(target_dir))
            
            # Should create target directory but no files
            assert target_dir.exists()
            assert len(list(target_dir.iterdir())) == 0

    def test_export_templates_path_expansion(self, temp_dir):
        """Test that paths are properly expanded."""
        # Use ~ in path to test expansion
        with patch('yaml2rst.initializer.TEMPLATE_DIR') as mock_template_dir, \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES') as mock_filenames, \
             patch('pathlib.Path.expanduser') as mock_expand:
            
            mock_template_dir = str(temp_dir / "builtin")
            mock_filenames = {'category_page': 'gl-category.rst'}
            mock_expand.return_value = temp_dir / "expanded"
            
            # Create source file
            builtin_dir = Path(mock_template_dir)
            builtin_dir.mkdir(parents=True, exist_ok=True)
            (builtin_dir / "gl-category.rst").write_text("test")
            
            export_templates("~/templates")
            
            # Verify expanduser was called
            mock_expand.assert_called()

    def test_export_templates_relative_path_resolution(self, temp_dir):
        """Test that relative paths are resolved correctly."""
        target_dir = temp_dir / "templates"
        
        with patch('yaml2rst.initializer.TEMPLATE_DIR') as mock_template_dir, \
             patch('yaml2rst.initializer.TEMPLATE_FILENAMES') as mock_filenames:
            
            mock_template_dir = str(temp_dir / "builtin")
            mock_filenames = {'category_page': 'gl-category.rst'}
            
            # Create source file
            builtin_dir = Path(mock_template_dir)
            builtin_dir.mkdir(parents=True, exist_ok=True)
            (builtin_dir / "gl-category.rst").write_text("test")
            
            # Use relative path
            export_templates("./templates")
            
            # Should still work (path gets resolved)
            # The exact location depends on current working directory,
            # but the function should not raise an error
