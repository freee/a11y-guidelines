"""Jinja2 template management for RST file generation.

This module provides the TemplateManager class for loading and rendering
Jinja2 templates to generate RST documentation files. It includes custom
filters for RST-specific formatting, particularly for creating properly
formatted headings that handle multibyte characters correctly.
"""
import unicodedata
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template


class TemplateManager:
    """Manages Jinja2 template loading and rendering for RST file generation.

    The TemplateManager handles the complete template workflow from loading
    templates with custom filters to rendering content and writing RST files.
    It provides specialized functionality for RST formatting, including
    proper handling of multibyte characters in headings.

    The manager automatically registers custom Jinja2 filters:
    - make_heading: Creates properly formatted RST headings with correct
      character width calculation for multibyte characters

    Attributes:
        env (Environment): Jinja2 environment with configured loader and
                          filters
        template (Optional[Template]): Currently loaded template instance

    Example:
        >>> template_manager = TemplateManager('/path/to/templates')
        >>> template_manager.load('category_page.j2')
        >>> data = {'title': 'カテゴリ', 'content': 'Content'}
        >>> template_manager.write_rst(data, '/output/category.rst')
    """

    def __init__(self, template_dir: str):
        """Initialize the template manager with a template directory.

        Sets up the Jinja2 environment with FileSystemLoader and registers
        custom filters for RST formatting.

        Args:
            template_dir: Path to the directory containing Jinja2 templates

        Example:
            >>> manager = TemplateManager('/project/templates')
            >>> # Templates can now be loaded from /project/templates/
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters['make_heading'] = self.make_heading
        self.template: Optional[Template] = None

    def load(self, filename: str) -> 'TemplateManager':
        """Load a Jinja2 template by filename.

        Loads the specified template file and stores it for rendering.
        Returns self to allow method chaining.

        Args:
            filename: Name of the template file to load (with or without .j2
                     extension)

        Returns:
            Self instance to allow method chaining

        Raises:
            TemplateNotFound: If the template file doesn't exist in the
                             template directory

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
