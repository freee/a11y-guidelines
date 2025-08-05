"""Configuration and initialization utilities for yaml2rst.

This module provides functions for setting up the yaml2rst conversion
environment, including command line argument parsing, directory structure
setup, template management, and variable configuration for the build system.

The initialization process follows a structured workflow:
1. Parse command line arguments to determine build mode and targets
2. Set up directory paths and file locations based on configuration
3. Initialize template management system
4. Configure build variables for Makefile generation

Functions:
    setup_parameters: Parse command line arguments and return settings
    setup_constants: Set up directory paths and file locations
    setup_variables: Initialize build variables for Makefile generation
    setup_templates: Initialize template management system
    parse_args: Parse command line arguments
    process_arguments: Process parsed arguments into settings dictionary
"""
import os
import argparse
from typing import Dict, Any, List, Tuple

from . import config
from .path import (get_dest_dirnames, get_static_dest_files, TEMPLATE_DIR,
                   TEMPLATE_FILENAMES)
from freee_a11y_gl.source import get_src_path
from .template_manager import TemplateManager
from .template_config import TemplateConfig


def setup_parameters() -> Dict[str, Any]:
    """Set up configuration parameters from command line arguments.

    Parses command line arguments and processes them into a configuration
    dictionary that controls the build process. This is the main entry
    point for configuration setup.

    Returns:
        Configuration dictionary containing:
        - build_all (bool): Whether to build all content or specific targets
        - targets (List[str]): List of specific files to build (if not
          build_all)
        - lang (str): Target language code ('ja', 'en', etc.)
        - basedir (str): Absolute path to the base directory containing data

    Example:
        >>> settings = setup_parameters()
        >>> print(settings['lang'])  # 'ja'
        >>> print(settings['build_all'])  # True or False
    """
    args = parse_args()
    return process_arguments(args)


def setup_constants(settings: Dict[str, Any]) -> Tuple[Dict[str, str],
                                                       Dict[str, str],
                                                       Dict[str, str]]:
    """Set up directory and file constants based on settings.

    Creates the directory structure and file path mappings needed for
    the conversion process. This includes output directories for different
    content types and static file locations.

    Args:
        settings: Configuration dictionary from setup_parameters()

    Returns:
        Tuple containing:
        - DEST_DIRS: Dictionary mapping content types to output directories
        - STATIC_FILES: Dictionary mapping file types to static file paths
        - MAKEFILE_VARS: Dictionary of variables for Makefile generation

    Example:
        >>> settings = {'lang': 'ja', 'basedir': '/data'}
        >>> dest_dirs, static_files, makefile_vars = setup_constants(settings)
        >>> print(dest_dirs['guidelines'])  # '/data/ja/source/categories'
    """
    lang = settings['lang']
    basedir = settings['basedir']
    DEST_DIRS = get_dest_dirnames(basedir, lang)
    STATIC_FILES = get_static_dest_files(basedir, lang)
    src_path = get_src_path(basedir)

    # Configure Makefile variables for build system integration
    # These variables are used in the generated Makefile to define
    # build targets and dependencies for Sphinx documentation
    MAKEFILE_VARS = {
        'all_checks_target': STATIC_FILES['all_checks'],
        'faq_index_target': " ".join([
            STATIC_FILES[key] for key in [
                'faq_index',
                'faq_tag_index',
                'faq_article_index'
            ]
        ]),
        'wcag_mapping_target': STATIC_FILES['wcag21mapping'],
        'priority_diff_target': STATIC_FILES['priority_diff'],
        'miscdefs_target': STATIC_FILES['miscdefs'],
        'wcag_sc': src_path['wcag_sc'],
        'info_src': src_path['info'],
        'axe_rules_target': STATIC_FILES['axe_rules'],
    }

    return DEST_DIRS, STATIC_FILES, MAKEFILE_VARS


def setup_variables() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """Initialize build variables for Makefile generation.

    Sets up the variable structures used by the MakefileGenerator to
    create build targets and dependencies. These variables are populated
    during the generation process and then used to create the final Makefile.

    Returns:
        Tuple containing:
        - makefile_vars: Dictionary of simple string variables
        - makefile_vars_list: Dictionary of list variables for multiple
          targets

    The variables include:
        Simple variables:
        - gl_yaml: Guideline YAML file paths
        - check_yaml: Check YAML file paths
        - faq_yaml: FAQ YAML file paths

        List variables:
        - guideline_category_target: Generated category page targets
        - check_example_target: Generated check example targets
        - faq_article_target: Generated FAQ article targets
        - faq_tagpage_target: Generated FAQ tag page targets
        - info_to_gl_target: Info-to-guideline cross-reference targets
        - info_to_faq_target: Info-to-FAQ cross-reference targets

    Example:
        >>> vars_dict, vars_list = setup_variables()
        >>> print(vars_dict.keys())  # dict_keys(['gl_yaml', 'check_yaml',
        ...                          #           'faq_yaml'])
        >>> print(vars_list.keys())  # dict_keys(['guideline_category_target',
        ...                          #           ...])
    """
    makefile_vars = {
        'gl_yaml': '',
        'check_yaml': '',
        'faq_yaml': ''
    }
    makefile_vars_list = {
        'guideline_category_target': [],
        'check_example_target': [],
        'faq_article_target': [],
        'faq_tagpage_target': [],
        'info_to_gl_target': [],
        'info_to_faq_target': [],
    }
    return makefile_vars, makefile_vars_list


def setup_templates(
    custom_template_dir: str = None
) -> Dict[str, TemplateManager]:
    """Set up template manager instances for all template files.

    Initializes TemplateManager instances for each template file defined
    in the TEMPLATE_FILENAMES configuration. Each template is pre-loaded
    and ready for use by the content generators.

    The function now supports the new template customization system, allowing
    users to override templates on a per-file basis while maintaining
    backward compatibility. It automatically loads configuration from files
    and environment variables.

    Args:
        custom_template_dir: Optional custom template directory path.
                           If provided, templates will be resolved with
                           priority: custom -> user -> built-in

    Returns:
        Dictionary mapping template names to loaded TemplateManager instances

    The returned dictionary contains entries for all templates:
    - category_page: For guideline category pages
    - faq_article: For individual FAQ articles
    - wcag21mapping: For WCAG mapping reference
    - makefile: For build system Makefile
    - And others as defined in TEMPLATE_FILENAMES

    Template Resolution Priority:
        1. Custom template directory (if specified via CLI --template-dir)
        2. User template directory (from config file or environment variable)
        3. Built-in template directory (src/yaml2rst/templates/)

    Configuration Sources (in order of precedence):
        1. CLI argument (--template-dir)
        2. Environment variables (YAML2RST_*)
        3. Configuration file (~/.config/freee_a11y_gl/yaml2rst.conf)
        4. Default values

    Example:
        >>> # Use default template resolution (loads config automatically)
        >>> templates = setup_templates()
        >>> category_template = templates['category_page']
        >>> category_template.write_rst(data, 'output.rst')

        >>> # Use custom template directory (overrides config)
        >>> templates = setup_templates('/custom/templates')
        >>> # Templates will be resolved from custom dir first
    """
    # Create template configuration and load from all sources
    config = TemplateConfig()

    # Set built-in template directory from the existing TEMPLATE_DIR
    from pathlib import Path
    config.built_in_template_dir = Path(TEMPLATE_DIR)

    # Set custom template directory if provided (CLI override)
    if custom_template_dir:
        config.custom_template_dir = custom_template_dir

    # Load configuration from file and environment variables
    # This will populate user_template_dir and other settings
    try:
        config.load_config()
    except Exception as e:
        # Log warning but continue with defaults
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to load template configuration: {e}")

    templates = {}
    for name, filename in TEMPLATE_FILENAMES.items():
        # Use the new template system with customizable resolution
        template_manager = TemplateManager.from_config(config)
        templates[name] = template_manager.load(filename)
    return templates


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the yaml2rst converter.

    Sets up the argument parser with all supported options and parses
    the command line arguments. The parser supports language selection,
    base directory specification, custom template directory, and optional
    file targeting.

    Returns:
        Parsed command line arguments as argparse.Namespace

    Supported Arguments:
        --lang, -l: Target language code (choices from
                    config.get_available_languages())
        --basedir, -b: Base directory containing the data directory
        --template-dir, -t: Custom template directory path
        files: Optional list of specific files to generate (positional)

    Example:
        Command line: python -m yaml2rst --lang en --basedir /data \\
                     --template-dir /custom/templates file1.rst
        >>> args = parse_args()
        >>> print(args.lang)  # 'en'
        >>> print(args.basedir)  # '/data'
        >>> print(args.template_dir)  # '/custom/templates'
        >>> print(args.files)  # ['file1.rst']
    """
    languages = config.get_available_languages()
    parser = argparse.ArgumentParser(
        description="Process YAML files into rst files for the "
                    "a11y-guidelines."
    )
    parser.add_argument(
        '--lang', '-l',
        type=str,
        choices=languages,
        default='ja',
        help=f'the language of the output file ({" ".join(languages)})'
    )
    parser.add_argument(
        '--basedir', '-b',
        type=str,
        default='..',
        help='Base directory where the data directory is located.'
    )
    parser.add_argument(
        '--template-dir', '-t',
        type=str,
        default=None,
        help='Custom template directory path. Templates in this directory '
             'will override built-in templates on a per-file basis.'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Filenames to generate (if not specified, generates all files)'
    )
    return parser.parse_args()


def process_arguments(args: argparse.Namespace) -> Dict[str, Any]:
    """Process parsed command-line arguments into a settings dictionary.

    Converts the argparse.Namespace object into a structured configuration
    dictionary and determines the build mode based on the presence of
    specific file arguments.

    Args:
        args: The parsed command-line arguments from parse_args()

    Returns:
        Dictionary containing processed settings:
        - build_all (bool): True if no specific files were specified
        - targets (List[str]): List of absolute paths to target files
        - lang (str): Target language code
        - basedir (str): Absolute path to the base directory
        - template_dir (str): Absolute path to custom template directory
                             (None if not specified)

    Build Mode Logic:
        - If no files are specified in args.files, build_all is True
        - If specific files are provided, build_all is False and targets
          contains the absolute paths to those files
        - The basedir and template_dir are always converted to absolute paths

    Example:
        >>> import argparse
        >>> args = argparse.Namespace(
        ...     lang='ja',
        ...     basedir='/data',
        ...     template_dir='/custom/templates',
        ...     files=['category.rst']
        ... )
        >>> settings = process_arguments(args)
        >>> print(settings)
        {
            'build_all': False,
            'targets': ['/absolute/path/to/category.rst'],
            'lang': 'ja',
            'basedir': '/absolute/path/to/data',
            'template_dir': '/absolute/path/to/custom/templates'
        }
    """
    basedir = os.path.abspath(args.basedir)
    template_dir = None
    if args.template_dir:
        template_dir = os.path.abspath(args.template_dir)

    files = []
    if args.files:
        files = [os.path.abspath(f) for f in args.files]

    return {
        'build_all': not args.files,
        'targets': files,
        'lang': args.lang,
        'basedir': basedir,
        'template_dir': template_dir
    }
