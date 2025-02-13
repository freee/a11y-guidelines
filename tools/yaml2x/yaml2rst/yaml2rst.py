#!/usr/bin/env python3
"""Convert YAML files into RST files for a11y-guidelines."""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import initializer
from generators.file_generator import FileGenerator, GeneratorConfig
from generators.content_generators import (
    CategoryGenerator,
    AllChecksGenerator, CheckExampleGenerator,
    FaqArticleGenerator, FaqTagPageGenerator, FaqIndexGenerator,
    FaqTagIndexGenerator, FaqArticleIndexGenerator,
    WcagMappingGenerator, PriorityDiffGenerator, MiscDefinitionsGenerator
)
from a11y_guidelines import setup_instances

def main():
    """Main entry point for the YAML to RST converter."""
    # Initialize settings and templates
    settings = initializer.setup_parameters()
    DEST_DIRS, STATIC_FILES, MAKEFILE_VARS = initializer.setup_constants(settings)
    templates = initializer.setup_templates()
    makefile_vars, makefile_vars_list = initializer.setup_variables()
    setup_instances(settings['basedir'])

    # Create output directories
    for directory in DEST_DIRS.values():
        os.makedirs(directory, exist_ok=True)

    # Initialize file generator
    file_generator = FileGenerator(templates, settings['lang'])

    # Configure generators
    generators = [
        # Guidelines and category generators
        GeneratorConfig(CategoryGenerator, 'category_page', DEST_DIRS['guidelines']),
        
        # Check generators
        GeneratorConfig(AllChecksGenerator, 'allchecks_text', STATIC_FILES['all_checks'], is_single_file=True),
        GeneratorConfig(CheckExampleGenerator, 'tool_example', DEST_DIRS['checks']),
        
        # FAQ generators
        GeneratorConfig(FaqArticleGenerator, 'faq_article', DEST_DIRS['faq_articles']),
        GeneratorConfig(FaqTagPageGenerator, 'faq_tagpage', DEST_DIRS['faq_tags']),
        GeneratorConfig(FaqIndexGenerator, 'faq_index', STATIC_FILES['faq_index'], is_single_file=True),
        GeneratorConfig(FaqTagIndexGenerator, 'faq_tag_index', STATIC_FILES['faq_tag_index'], is_single_file=True),
        GeneratorConfig(FaqArticleIndexGenerator, 'faq_article_index', STATIC_FILES['faq_article_index'], is_single_file=True),
        
        # Reference generators
        GeneratorConfig(WcagMappingGenerator, 'wcag21mapping', STATIC_FILES['wcag21mapping'], is_single_file=True),
        GeneratorConfig(PriorityDiffGenerator, 'priority_diff', STATIC_FILES['priority_diff'], is_single_file=True),
        GeneratorConfig(MiscDefinitionsGenerator, 'miscdefs', STATIC_FILES['miscdefs'], is_single_file=True)
    ]

    # Generate all files
    for config in generators:
        file_generator.generate(config, settings['build_all'], settings['targets'])

    # Generate makefile with special handling
    makefile_extra_vars = {
        'DEST_DIRS': DEST_DIRS,
        'MAKEFILE_VARS': MAKEFILE_VARS,
        'makefile_vars': makefile_vars,
        'makefile_vars_list': makefile_vars_list
    }
    file_generator.generate_makefile(
        templates['makefile'],
        STATIC_FILES['makefile'],
        settings['build_all'],
        settings['targets'],
        makefile_extra_vars
    )

if __name__ == "__main__":
    main()
