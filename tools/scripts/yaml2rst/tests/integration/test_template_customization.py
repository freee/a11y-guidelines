"""Integration tests for template customization system."""
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from yaml2rst.template_manager import TemplateManager
from yaml2rst.template_config import TemplateConfig
from yaml2rst.template_resolver import TemplateResolver
from yaml2rst.initializer import setup_templates


class TestTemplateCustomizationIntegration:
    """Integration tests for the complete template customization workflow."""

    def setup_method(self):
        """Set up test directories and files."""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.builtin_dir = Path(self.temp_dir) / "builtin"
        self.user_dir = Path(self.temp_dir) / "user"
        self.custom_dir = Path(self.temp_dir) / "custom"

        # Create directories
        self.builtin_dir.mkdir(parents=True)
        self.user_dir.mkdir(parents=True)
        self.custom_dir.mkdir(parents=True)

        # Create test template files
        self.create_test_templates()

    def teardown_method(self):
        """Clean up test directories."""
        shutil.rmtree(self.temp_dir)

    def create_test_templates(self):
        """Create test template files in different directories."""
        # Built-in template
        builtin_template = self.builtin_dir / "test-template.rst"
        builtin_template.write_text("Built-in: {{ title }}")

        # User template (overrides built-in)
        user_template = self.user_dir / "test-template.rst"
        user_template.write_text("User: {{ title }}")

        # Custom template (overrides both)
        custom_template = self.custom_dir / "test-template.rst"
        custom_template.write_text("Custom: {{ title }}")

        # Template only in built-in
        builtin_only = self.builtin_dir / "builtin-only.rst"
        builtin_only.write_text("Built-in only: {{ content }}")

    def test_template_resolution_priority(self):
        """Test that template resolution follows correct priority order."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir
        config.user_template_dir = self.user_dir
        config.custom_template_dir = str(self.custom_dir)

        resolver = TemplateResolver(
            custom_template_dir=str(self.custom_dir),
            template_config=config
        )

        # Should resolve to custom template (highest priority)
        resolved_path = resolver.resolve_template("test-template.rst")
        assert resolved_path == str(self.custom_dir / "test-template.rst")

        # Should resolve to built-in template (only available there)
        resolved_path = resolver.resolve_template("builtin-only.rst")
        assert resolved_path == str(self.builtin_dir / "builtin-only.rst")

    def test_template_resolution_without_custom(self):
        """Test template resolution without custom directory."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir
        config.user_template_dir = self.user_dir

        resolver = TemplateResolver(template_config=config)

        # Should resolve to user template (higher priority than built-in)
        resolved_path = resolver.resolve_template("test-template.rst")
        assert resolved_path == str(self.user_dir / "test-template.rst")

    def test_template_resolution_builtin_only(self):
        """Test template resolution with only built-in templates."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir

        resolver = TemplateResolver(template_config=config)

        # Should resolve to built-in template
        resolved_path = resolver.resolve_template("test-template.rst")
        assert resolved_path == str(self.builtin_dir / "test-template.rst")

    def test_template_manager_integration(self):
        """Test TemplateManager integration with custom templates."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir
        config.user_template_dir = self.user_dir
        config.custom_template_dir = str(self.custom_dir)

        manager = TemplateManager.from_config(config)
        manager.load("test-template.rst")

        # Render template with data
        data = {"title": "Integration Test"}

        # Create temporary output file
        output_file = Path(self.temp_dir) / "output.rst"
        manager.write_rst(data, str(output_file))

        # Verify content comes from custom template
        content = output_file.read_text()
        assert content == "Custom: Integration Test"

    def test_template_manager_backward_compatibility(self):
        """Test that TemplateManager maintains backward compatibility."""
        # Create a simple template in builtin directory
        template_file = self.builtin_dir / "simple.rst"
        template_file.write_text("Simple: {{ message }}")

        # Use old-style constructor
        manager = TemplateManager(str(self.builtin_dir))
        manager.load("simple.rst")

        # Render template
        data = {"message": "Hello World"}
        output_file = Path(self.temp_dir) / "simple_output.rst"
        manager.write_rst(data, str(output_file))

        # Verify content
        content = output_file.read_text()
        assert content == "Simple: Hello World"

    def test_setup_templates_integration(self):
        """Test setup_templates function with custom directory."""
        # Mock TEMPLATE_FILENAMES to use our test templates
        mock_template_filenames = {
            'test_template': 'test-template.rst',
            'builtin_only': 'builtin-only.rst'
        }

        with patch('yaml2rst.initializer.TEMPLATE_FILENAMES',
                   mock_template_filenames), \
             patch('yaml2rst.initializer.TEMPLATE_DIR', str(self.builtin_dir)):

            # Test with custom template directory
            templates = setup_templates(str(self.custom_dir))

            # Verify templates were loaded
            assert 'test_template' in templates
            assert 'builtin_only' in templates

            # Test rendering with custom template
            data = {"title": "Setup Test"}
            output_file = Path(self.temp_dir) / "setup_output.rst"
            templates['test_template'].write_rst(data, str(output_file))

            # Should use custom template
            content = output_file.read_text()
            assert content == "Custom: Setup Test"

            # Test rendering with builtin-only template
            data = {"content": "Builtin Content"}
            output_file2 = Path(self.temp_dir) / "builtin_output.rst"
            templates['builtin_only'].write_rst(data, str(output_file2))

            # Should use builtin template
            content = output_file2.read_text()
            assert content == "Built-in only: Builtin Content"

    def test_template_not_found_error(self):
        """Test error handling when template is not found."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir

        resolver = TemplateResolver(template_config=config)

        with pytest.raises(Exception):  # TemplateNotFoundError
            resolver.resolve_template("nonexistent-template.rst")

    def test_template_source_info(self):
        """Test getting template source information."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir
        config.user_template_dir = self.user_dir
        config.custom_template_dir = str(self.custom_dir)

        resolver = TemplateResolver(
            custom_template_dir=str(self.custom_dir),
            template_config=config
        )

        # Get source info for custom template
        info = resolver.get_template_source_info("test-template.rst")
        assert info['source_type'] == 'custom'
        assert info['template_name'] == 'test-template.rst'

        # Get source info for builtin-only template
        info = resolver.get_template_source_info("builtin-only.rst")
        assert info['source_type'] == 'builtin'
        assert info['template_name'] == 'builtin-only.rst'

    def test_template_conflicts_detection(self):
        """Test detection of template conflicts."""
        config = TemplateConfig()
        config.built_in_template_dir = self.builtin_dir
        config.user_template_dir = self.user_dir
        config.custom_template_dir = str(self.custom_dir)

        resolver = TemplateResolver(
            custom_template_dir=str(self.custom_dir),
            template_config=config
        )

        conflicts = resolver.find_template_conflicts()

        # test-template.rst should be in conflict (exists in all three dirs)
        assert "test-template.rst" in conflicts
        assert len(conflicts["test-template.rst"]) == 3  # all three sources

        # builtin-only.rst should not be in conflict
        assert "builtin-only.rst" not in conflicts
