"""Jinja2 template management for RST file generation.

This module provides the TemplateManager class for loading and rendering
Jinja2 templates to generate RST documentation files. It includes custom
filters for RST-specific formatting, particularly for creating properly
formatted headings that handle multibyte characters correctly.

The TemplateManager now supports customizable template resolution through
the TemplateResolver system, allowing users to override templates on a
per-file basis while maintaining backward compatibility.
"""
import unicodedata
from typing import Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, Template

from .template_resolver import TemplateResolver
from .template_config import TemplateConfig


class TemplateManager:
    """Manages Jinja2 template loading and rendering for RST file generation.

    The TemplateManager handles the complete template workflow from loading
    templates with custom filters to rendering content and writing RST files.
    It provides specialized functionality for RST formatting, including
    proper handling of multibyte characters in headings.

    The manager now supports customizable template resolution through the
    TemplateResolver system, allowing users to override templates on a
    per-file basis while maintaining backward compatibility.

    The manager automatically registers custom Jinja2 filters:
    - make_heading: Creates properly formatted RST headings with correct
      character width calculation for multibyte characters

    Attributes:
        resolver (TemplateResolver): Template resolver for finding templates
        env (Environment): Jinja2 environment with configured loader and
                          filters
        template (Optional[Template]): Currently loaded template instance

    Example:
        >>> # Legacy usage (backward compatible)
        >>> template_manager = TemplateManager('/path/to/templates')
        >>> template_manager.load('category_page.j2')
        >>> data = {'title': 'カテゴリ', 'content': 'Content'}
        >>> template_manager.write_rst(data, '/output/category.rst')

        >>> # New usage with custom template directory
        >>> config = TemplateConfig(custom_template_dir='/custom/templates')
        >>> template_manager = TemplateManager.from_config(config)
        >>> template_manager.load('category_page.j2')
    """

    def __init__(self, template_dir: str):
        """Initialize the template manager with a template directory.

        Sets up the Jinja2 environment with FileSystemLoader and registers
        custom filters for RST formatting. This constructor maintains
        backward compatibility with the original API.

        Args:
            template_dir: Path to the directory containing Jinja2 templates

        Example:
            >>> manager = TemplateManager('/project/templates')
            >>> # Templates can now be loaded from /project/templates/
        """
        # For backward compatibility, create a template config with only
        # the built-in template directory and use the resolver
        config = TemplateConfig()
        config.built_in_template_dir = Path(template_dir)

        self.resolver = TemplateResolver(template_config=config)
        self._setup_jinja_environment()
        self.template: Optional[Template] = None

    @classmethod
    def from_config(
            cls, config: Optional[TemplateConfig] = None) -> 'TemplateManager':
        """Create a TemplateManager instance from a TemplateConfig.

        This is the recommended way to create a TemplateManager when using
        the new template customization features.

        Args:
            config: Template configuration. If None, uses default
                   configuration.

        Returns:
            TemplateManager instance configured with the specified settings

        Example:
            >>> config = TemplateConfig(
                custom_template_dir='/custom/templates')
            >>> manager = TemplateManager.from_config(config)
            >>> manager.load('category_page.j2')
        """
        if config is None:
            config = TemplateConfig()

        # Create instance and set up resolver
        instance = cls.__new__(cls)
        instance.resolver = TemplateResolver(template_config=config)
        instance._setup_jinja_environment()
        instance.template = None
        return instance

    def _setup_jinja_environment(self) -> None:
        """Set up the Jinja2 environment with custom loader and filters."""
        # Create a custom loader that uses the resolver
        class ResolverLoader:
            def __init__(self, resolver: TemplateResolver):
                self.resolver = resolver

            def get_source(self, environment, template):
                try:
                    template_path = self.resolver.resolve_template(template)
                    with open(template_path, 'r', encoding='utf-8') as f:
                        source = f.read()

                    # Return source, filename, and uptodate function
                    def uptodate():
                        try:
                            return Path(template_path).stat().st_mtime
                        except OSError:
                            return False

                    return source, str(template_path), uptodate
                except Exception as e:
                    from jinja2 import TemplateNotFound
                    raise TemplateNotFound(template) from e

            def load(self, environment, name, globals=None):
                """Load method required by Jinja2."""
                source, filename, uptodate = self.get_source(environment, name)
                code = environment.compile(source, name, filename)
                return environment.template_class.from_code(
                    environment, code, globals, uptodate)

        self.env = Environment(loader=ResolverLoader(self.resolver))
        self.env.filters['make_heading'] = self.make_heading

    def load(self, filename: str) -> 'TemplateManager':
        """Load a Jinja2 template by filename.

        Loads the specified template file using the template resolver and
        stores it for rendering. Returns self to allow method chaining.

        The template is resolved using the priority order:
        1. Custom template directory (if specified)
        2. User template directory (~/.config/freee_a11y_gl/templates/)
        3. Built-in template directory

        Args:
            filename: Name of the template file to load (with or without .j2
                     extension)

        Returns:
            Self instance to allow method chaining

        Raises:
            TemplateNotFound: If the template file doesn't exist in any
                             of the configured template directories

        Example:
            >>> manager = TemplateManager('/templates')
            >>> manager.load('category_page.j2').write_rst(data, 'output.rst')
        """
        self.template = self.env.get_template(filename)
        return self

    def write_rst(self, data: Dict[str, Any], output_path: str) -> None:
        """Render the loaded template with data and write to an RST file.

        Takes the currently loaded template, renders it with the provided data,
        and writes the result to the specified output file with UTF-8 encoding
        and Unix line endings.

        Args:
            data: Dictionary containing template variables and their values
            output_path: Path where the rendered RST file will be written

        Raises:
            AttributeError: If no template has been loaded via load() method
            IOError: If the output file cannot be written

        Example:
            >>> data = {
            ...     'title': 'Page Title',
            ...     'categories': [{'name': 'Category 1', 'items': [...]}]
            ... }
            >>> manager.load('page_template.j2')
            >>> manager.write_rst(data, '/output/page.rst')
        """
        if self.template is None:
            raise AttributeError("No template loaded. Call load() first.")

        rendered_content = self.template.render(data)
        with open(output_path, mode='w', encoding='utf-8',
                  newline='\n') as file:
            file.write(rendered_content)

    @staticmethod
    def make_heading(title: str, level: int, class_name: str = "") -> str:
        """Create a properly formatted RST heading with multibyte support.

        Generates RST headings with correct underline/overline character counts
        that account for the display width of multibyte characters (such as
        Japanese, Chinese, Korean characters). This ensures proper visual
        alignment in rendered documentation.

        The method supports 6 heading levels with different character styles:
        1. # with overline (top level)
        2. * with overline
        3. = underline only
        4. - underline only
        5. ^ underline only
        6. " underline only

        Args:
            title: The heading text (may contain multibyte characters)
            level: Heading level from 1 (highest) to 6 (lowest)
            class_name: Optional CSS class name for the heading

        Returns:
            Formatted RST heading string with proper line lengths

        Raises:
            ValueError: If level is not between 1 and 6

        Example:
            >>> heading = TemplateManager.make_heading('カテゴリ', 1)
            >>> print(heading)
            ########
            カテゴリ
            ########

            >>> heading = TemplateManager.make_heading('Section', 3,
            ...                                        'custom-class')
            >>> print(heading)
            .. rst-class:: custom-class

            Section
            =======
        """

        def _is_multibyte(c: str) -> bool:
            """Check if character is multibyte."""
            return unicodedata.east_asian_width(c) in ['F', 'W', 'A']

        def _width(c: str) -> int:
            """Get display width of character (2 for multibyte, 1 others)."""
            return 2 if _is_multibyte(c) else 1

        def width(s: str) -> int:
            """Calculate the total display width of a string."""
            return sum(_width(c) for c in s)

        # Define heading styles: (character, has_overline)
        heading_styles = [
            ('#', True),   # Level 1: # with overline
            ('*', True),   # Level 2: * with overline
            ('=', False),  # Level 3: = underline only
            ('-', False),  # Level 4: - underline only
            ('^', False),  # Level 5: ^ underline only
            ('"', False),  # Level 6: " underline only
        ]

        if not 1 <= level <= len(heading_styles):
            raise ValueError(f'Invalid level: {level}. Must be between 1 and '
                             f'{len(heading_styles)}')

        char, overline = heading_styles[level - 1]
        line = char * width(title)

        heading_lines = []

        # Add CSS class directive if specified
        if class_name:
            heading_lines.append(f'.. rst-class:: {class_name}\n')

        # Add overline for levels 1 and 2
        if overline:
            heading_lines.append(line)

        # Add title and underline
        heading_lines.append(title)
        heading_lines.append(line)

        return '\n'.join(heading_lines)
