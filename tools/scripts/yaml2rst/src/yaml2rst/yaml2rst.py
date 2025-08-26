#!/usr/bin/env python3
"""Convert YAML files into RST files for a11y-guidelines.

This is the main entry point for the yaml2rst package, which converts
accessibility guideline data from YAML format into reStructuredText (RST)
files for Sphinx documentation generation.

The module orchestrates the complete conversion workflow:
1. Initialize configuration and templates
2. Set up the freee_a11y_gl library with yaml2rst profile
3. Configure and run multiple content generators
4. Generate RST files for guidelines, checks, FAQs, and reference materials

Architecture:
    The conversion process uses a modular generator architecture where each
    content type (categories, checks, FAQs, etc.) has its own specialized
    generator class. All generators inherit from ContentGeneratorBase and
    use shared mixins for common functionality.

Supported Content Types:
    - Category pages with associated guidelines
    - Check items and examples
    - FAQ articles and tag pages
    - WCAG mapping and reference documentation
    - Build system files (Makefile)

Example:
    Run the converter for Japanese output:
    $ python -m yaml2rst --lang ja --basedir /path/to/data

    Generate specific files only:
    $ python -m yaml2rst --lang en category_page.rst faq_index.rst
"""
import os

from . import initializer
from .generators.file_generator import FileGenerator, GeneratorConfig
from .generators.content_generators import (
    CategoryGenerator,
    AllChecksGenerator, CheckExampleGenerator,
    FaqArticleGenerator, FaqTagPageGenerator, FaqIndexGenerator,
    FaqTagIndexGenerator, FaqArticleIndexGenerator,
    WcagMappingGenerator, PriorityDiffGenerator, MiscDefinitionsGenerator,
    InfoToGuidelinesGenerator, InfoToFaqsGenerator,
    AxeRulesGenerator,
    MakefileGenerator,
    MakefileConfig
)
from freee_a11y_gl import setup_instances
from freee_a11y_gl.config import Config


def main() -> None:
    """Main entry point for the YAML to RST converter.

    Orchestrates the complete conversion workflow from YAML source files
    to RST documentation files. This function:

    1. Parses command line arguments and sets up configuration
    2. Initializes the freee_a11y_gl library with yaml2rst profile
    3. Creates output directories
    4. Configures all content generators
    5. Runs the file generation process
    6. Generates the build system Makefile

    The conversion process supports both full builds (all content) and
    targeted builds (specific files only) based on command line arguments.

    Workflow:
        1. Configuration Setup:
           - Parse command line arguments (language, base directory, targets)
           - Set up directory paths and template system
           - Initialize freee_a11y_gl with yaml2rst profile

        2. Content Generation:
           - Create FileGenerator instance for the target language
           - Configure all generator classes with their templates and output
             paths
           - Run generators based on build mode (all or targeted)

        3. Build System:
           - Generate Makefile with proper dependencies and targets
           - Set up build variables for Sphinx integration

    Raises:
        SystemExit: If command line arguments are invalid
        OSError: If output directories cannot be created
        ConfigurationError: If freee_a11y_gl initialization fails

    Example:
        >>> # This function is typically called via command line:
        >>> # python -m yaml2rst --lang ja --basedir /data
        >>> main()  # Processes all content for Japanese
    """
    # Initialize settings and templates
    settings = initializer.setup_parameters()
    DEST_DIRS, STATIC_FILES, MAKEFILE_VARS = initializer.setup_constants(
        settings)
    templates = initializer.setup_templates(settings.get('template_dir'))
    makefile_vars, makefile_vars_list = initializer.setup_variables()

    # Initialize freee_a11y_gl configuration with yaml2rst profile
    # This sets up the library to work with our specific data structure
    # and provides access to guideline, check, and FAQ data
    Config.initialize(
        profile="yaml2rst",
        config_override={
            "basedir": settings['basedir'],
            "languages": {
                "default": settings['lang']
            }
        }
    )

    # Initialize core settings and load data
    # This populates the RelationshipManager with all guideline data
    setup_instances(settings['basedir'])

    # Create output directories for generated files
    # Ensures all destination paths exist before generation begins
    for directory in DEST_DIRS.values():
        os.makedirs(directory, exist_ok=True)

    # Initialize file generator for the target language
    # The FileGenerator orchestrates the template rendering and file writing
    file_generator = FileGenerator(templates, settings['lang'])

    # Configure all content generators with their templates and output paths
    # Each GeneratorConfig specifies:
    # - Generator class to instantiate
    # - Template name to use for rendering
    # - Output path for generated files
    # - Whether the generator produces a single file or multiple files
    generators = [
        # Guidelines and category generators
        # Generates individual category pages with associated guidelines
        GeneratorConfig(CategoryGenerator, 'category_page',
                        DEST_DIRS['guidelines']),

        # Check generators
        # AllChecksGenerator creates a single file with all check items
        GeneratorConfig(AllChecksGenerator, 'allchecks_text',
                        STATIC_FILES['all_checks'], is_single_file=True),
        # CheckExampleGenerator creates individual example files
        GeneratorConfig(CheckExampleGenerator, 'tool_example',
                        DEST_DIRS['checks']),

        # FAQ generators
        # Individual FAQ article pages
        GeneratorConfig(FaqArticleGenerator, 'faq_article',
                        DEST_DIRS['faq_articles']),
        # FAQ tag pages (articles grouped by tag)
        GeneratorConfig(FaqTagPageGenerator, 'faq_tagpage',
                        DEST_DIRS['faq_tags']),
        # FAQ index pages (single files with navigation)
        GeneratorConfig(FaqIndexGenerator, 'faq_index',
                        STATIC_FILES['faq_index'], is_single_file=True),
        GeneratorConfig(FaqTagIndexGenerator, 'faq_tag_index',
                        STATIC_FILES['faq_tag_index'], is_single_file=True),
        GeneratorConfig(FaqArticleIndexGenerator, 'faq_article_index',
                        STATIC_FILES['faq_article_index'],
                        is_single_file=True),

        # Info reference generators
        # Cross-reference pages linking info to guidelines and FAQs
        GeneratorConfig(InfoToGuidelinesGenerator, 'info_to_gl',
                        DEST_DIRS['info2gl']),
        GeneratorConfig(InfoToFaqsGenerator, 'info_to_faq',
                        DEST_DIRS['info2faq']),

        # Reference generators
        # Single-file reference documentation
        GeneratorConfig(WcagMappingGenerator, 'wcag21mapping',
                        STATIC_FILES['wcag21mapping'], is_single_file=True),
        GeneratorConfig(PriorityDiffGenerator, 'priority_diff',
                        STATIC_FILES['priority_diff'], is_single_file=True),
        GeneratorConfig(MiscDefinitionsGenerator, 'miscdefs',
                        STATIC_FILES['miscdefs'], is_single_file=True),
        GeneratorConfig(AxeRulesGenerator, 'axe_rules',
                        STATIC_FILES['axe_rules'], is_single_file=True),
    ]

    # Generate all content files
    # Each generator processes its data and creates the appropriate RST files
    for config in generators:
        file_generator.generate(config, settings['build_all'],
                                settings['targets'])

    # Generate Makefile (once, outside the main loop)
    # The Makefile contains build targets and dependencies for Sphinx
    makefile_config = MakefileConfig(
        dest_dirs=DEST_DIRS,
        makefile_vars=MAKEFILE_VARS,
        base_vars=makefile_vars,
        vars_list=makefile_vars_list
    )
    makefile_generator = GeneratorConfig(
        MakefileGenerator,
        'makefile',
        STATIC_FILES['makefile'],
        is_single_file=True,
        extra_args={'config': makefile_config}
    )
    file_generator.generate(makefile_generator, settings['build_all'],
                            settings['targets'])


if __name__ == "__main__":
    main()
