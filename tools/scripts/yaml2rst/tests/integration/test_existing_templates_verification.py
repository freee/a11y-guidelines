"""Integration tests for template customization with existing templates.

This module tests the complete template customization workflow using actual
existing template files to verify that the system works correctly with
real templates in production scenarios.
"""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from yaml2rst.initializer import setup_templates
from yaml2rst.template_config import TemplateConfig
from yaml2rst.template_manager import TemplateManager
from yaml2rst.path import TEMPLATE_DIR


class TestExistingTemplatesVerification:
    """Test template customization with actual existing templates."""

    def test_builtin_templates_exist(self):
        """Verify that all expected built-in templates exist."""
        template_dir = Path(TEMPLATE_DIR)

        # Check that the template directory exists
        template_dir_msg = f"Template directory not found: {template_dir}"
        assert template_dir.exists(), template_dir_msg

        # Check for key template files
        expected_templates = [
            'gl-category.rst',
            'wcag21-mapping.rst',
            'axe-rules.rst',
            'misc-defs.txt',
            'priority-diff.rst',
            'info_to_gl.rst',
            'info_to_faq.rst',
            'incfiles.mk'
        ]

        for template_name in expected_templates:
            template_path = template_dir / template_name
            template_msg = f"Expected template not found: {template_name}"
            assert template_path.exists(), template_msg

    def test_template_customization_with_existing_templates(self):
        """Test template customization using actual existing templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create custom template directory
            custom_dir = Path(temp_dir) / "custom"
            custom_dir.mkdir()

            # Create a customized version of gl-category.rst
            custom_template = custom_dir / "gl-category.rst"
            custom_template.write_text("""
**CUSTOM TEMPLATE LOADED**

{% for gl in guidelines -%}
Custom GL: {{ gl.title }}
{{ gl.guideline }}
{% endfor %}
""")

            # Test template resolution with custom directory
            config = TemplateConfig()
            config.custom_template_dir = str(custom_dir)
            config.built_in_template_dir = Path(TEMPLATE_DIR)

            # Create template manager and load template
            manager = TemplateManager.from_config(config)
            template = manager.load("gl-category.rst")

            # Verify the custom template was loaded by reading resolved file
            gl_resolved = template.resolver.resolve_template("gl-category.rst")
            with open(gl_resolved, 'r') as f:
                template_content = f.read()
            assert "**CUSTOM TEMPLATE LOADED**" in template_content
            assert "Custom GL:" in template_content

    def test_template_fallback_to_builtin(self):
        """Test templates fall back to built-in when custom doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create custom template directory with only one custom template
            custom_dir = Path(temp_dir) / "custom"
            custom_dir.mkdir()

            # Create custom gl-category.rst but not wcag21-mapping.rst
            custom_template = custom_dir / "gl-category.rst"
            custom_template.write_text("**CUSTOM GL TEMPLATE**")

            # Test template resolution
            config = TemplateConfig()
            config.custom_template_dir = str(custom_dir)
            config.built_in_template_dir = Path(TEMPLATE_DIR)

            manager = TemplateManager.from_config(config)

            # Load custom template
            gl_template = manager.load("gl-category.rst")
            gl_resolved = gl_template.resolver.resolve_template(
                "gl-category.rst")
            with open(gl_resolved, 'r') as f:
                gl_content = f.read()
            assert "**CUSTOM GL TEMPLATE**" in gl_content

            # Load built-in template (fallback)
            wcag_template = manager.load("wcag21-mapping.rst")
            wcag_resolved = wcag_template.resolver.resolve_template(
                "wcag21-mapping.rst")
            with open(wcag_resolved, 'r') as f:
                wcag_content = f.read()
            # Should contain built-in content, not custom content
            assert "**CUSTOM GL TEMPLATE**" not in wcag_content

    def test_setup_templates_with_existing_templates(self):
        """Test setup_templates function with actual existing templates."""
        # Test default setup (no custom directory)
        templates = setup_templates()

        # Verify that all expected templates are loaded
        expected_template_names = [
            'category_page',  # maps to gl-category.rst
            'wcag21mapping',  # maps to wcag21-mapping.rst
            'axe_rules',      # maps to axe-rules.rst
            'miscdefs',       # maps to misc-defs.txt
            'priority_diff',  # maps to priority-diff.rst
            'info_to_gl',     # maps to info_to_gl.rst
            'info_to_faq',    # maps to info_to_faq.rst
            'makefile'        # maps to incfiles.mk
        ]

        for template_name in expected_template_names:
            template_msg = f"Template not loaded: {template_name}"
            assert template_name in templates, template_msg
            assert templates[template_name] is not None

    def test_setup_templates_with_custom_directory(self):
        """Test setup_templates with custom template directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_dir = Path(temp_dir) / "custom"
            custom_dir.mkdir()

            # Create a custom version of gl-category.rst
            custom_template = custom_dir / "gl-category.rst"
            custom_template.write_text("**CUSTOM CATEGORY TEMPLATE**")

            # Test setup_templates with custom directory
            templates = setup_templates(str(custom_dir))

            # Verify custom template is used
            category_template = templates['category_page']
            gl_resolved = category_template.resolver.resolve_template(
                "gl-category.rst")
            with open(gl_resolved, 'r') as f:
                template_content = f.read()
            assert "**CUSTOM CATEGORY TEMPLATE**" in template_content

    def test_configuration_file_integration_with_existing_templates(self):
        """Test configuration file integration with existing templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config file
            config_file = Path(temp_dir) / "yaml2rst.conf"
            config_file.write_text("""[templates]
user_template_dir = {}/user_templates
fallback_to_builtin = true
""".format(temp_dir))

            # Create user template directory
            user_dir = Path(temp_dir) / "user_templates"
            user_dir.mkdir()

            # Create custom template
            user_template = user_dir / "gl-category.rst"
            user_template.write_text("**USER CONFIG TEMPLATE**")

            # Test with custom config file
            config = TemplateConfig(str(config_file))
            config.built_in_template_dir = Path(TEMPLATE_DIR)

            # Load configuration
            loaded_config = config.load_config()
            expected_dir = f"{temp_dir}/user_templates"
            assert loaded_config['user_template_dir'] == expected_dir

            # Test template resolution
            manager = TemplateManager.from_config(config)
            template = manager.load("gl-category.rst")

            # Verify user template was loaded
            gl_resolved = template.resolver.resolve_template("gl-category.rst")
            with open(gl_resolved, 'r') as f:
                template_content = f.read()
            assert "**USER CONFIG TEMPLATE**" in template_content

    def test_environment_variable_integration(self):
        """Test environment variable integration with existing templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create user template directory
            user_dir = Path(temp_dir) / "env_templates"
            user_dir.mkdir()

            # Create custom template
            env_template = user_dir / "gl-category.rst"
            env_template.write_text("**ENV VAR TEMPLATE**")

            # Test with environment variable
            with patch.dict(os.environ, {
                'YAML2RST_USER_TEMPLATE_DIR': str(user_dir),
                'YAML2RST_FALLBACK_TO_BUILTIN': 'true'
            }):
                config = TemplateConfig()
                config.built_in_template_dir = Path(TEMPLATE_DIR)

                # Load configuration
                loaded_config = config.load_config()
                assert loaded_config['user_template_dir'] == str(user_dir)

                # Test template resolution
                manager = TemplateManager.from_config(config)
                template = manager.load("gl-category.rst")

                # Verify environment template was loaded
                gl_resolved = template.resolver.resolve_template(
                    "gl-category.rst")
                with open(gl_resolved, 'r') as f:
                    template_content = f.read()
                assert "**ENV VAR TEMPLATE**" in template_content

    def test_template_priority_with_all_sources(self):
        """Test template priority with custom, user, and built-in sources."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create all three template sources
            custom_dir = Path(temp_dir) / "custom"
            user_dir = Path(temp_dir) / "user"
            custom_dir.mkdir()
            user_dir.mkdir()

            # Create templates in each source
            (custom_dir / "gl-category.rst").write_text("**CUSTOM PRIORITY**")
            (user_dir / "gl-category.rst").write_text("**USER PRIORITY**")

            # Create config file pointing to user directory
            config_file = Path(temp_dir) / "yaml2rst.conf"
            config_file.write_text(f"""[templates]
user_template_dir = {user_dir}
fallback_to_builtin = true
""")

            # Test priority: custom > user > built-in
            config = TemplateConfig(str(config_file))
            config.custom_template_dir = str(custom_dir)
            config.built_in_template_dir = Path(TEMPLATE_DIR)

            manager = TemplateManager.from_config(config)
            template = manager.load("gl-category.rst")

            # Should load custom template (highest priority)
            gl_resolved = template.resolver.resolve_template("gl-category.rst")
            with open(gl_resolved, 'r') as f:
                template_content = f.read()
            assert "**CUSTOM PRIORITY**" in template_content
            assert "**USER PRIORITY**" not in template_content

    def test_template_source_information(self):
        """Test that template source information is correctly tracked."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_dir = Path(temp_dir) / "custom"
            custom_dir.mkdir()

            # Create custom template
            custom_template = custom_dir / "gl-category.rst"
            custom_template.write_text("**CUSTOM TEMPLATE**")

            # Test template loading with source tracking
            config = TemplateConfig()
            config.custom_template_dir = str(custom_dir)
            config.built_in_template_dir = Path(TEMPLATE_DIR)

            manager = TemplateManager.from_config(config)
            template = manager.load("gl-category.rst")

            # Verify source information - check resolver has correct path
            gl_resolved = template.resolver.resolve_template("gl-category.rst")
            assert str(custom_template) == str(gl_resolved)
