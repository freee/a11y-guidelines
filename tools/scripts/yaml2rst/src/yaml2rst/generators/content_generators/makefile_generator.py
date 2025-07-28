"""Makefile generator for managing build dependencies.

This module provides specialized generators for creating Makefile content
that manages build dependencies for the accessibility guidelines documentation
system. It processes various data sources to generate comprehensive dependency
tracking for automated build systems.

The module integrates with multiple freee_a11y_gl models to collect dependency
information and generates Makefile content with:
- Source file dependency tracking
- Target file generation rules
- Variable definitions for build automation
- Comprehensive error handling and validation

Classes:
    MakefileConfig: Configuration dataclass for Makefile generation
    MakefileGenerator: Main generator for Makefile content with dependencies
"""
from typing import Dict, Any, List
import os
from dataclasses import dataclass

from freee_a11y_gl import (
    Category, CheckTool, Faq, FaqTag, InfoRef,
    Guideline, Check
)
from ..content_generator_base import ContentGeneratorBase


@dataclass
class MakefileConfig:
    """Configuration for Makefile generation.

    This dataclass encapsulates all configuration parameters needed for
    Makefile generation, including directory mappings, variable definitions,
    and build system settings. It provides a structured way to pass
    configuration data to the MakefileGenerator.

    Attributes:
        dest_dirs (Dict[str, str]): Mapping of content types to destination
            directories
        makefile_vars (Dict[str, str]): Makefile variable definitions
        base_vars (Dict[str, str]): Base variable definitions for the build
            system
        vars_list (Dict[str, List[str]]): Lists of variables for different
            content types

    Example:
        >>> config = MakefileConfig(
        ...     dest_dirs={'guidelines': 'source/categories'},
        ...     makefile_vars={'LANG': 'ja'},
        ...     base_vars={'SRC_DIR': 'data/yaml'},
        ...     vars_list={'targets': ['all', 'clean']}
        ... )
    """
    dest_dirs: Dict[str, str]
    makefile_vars: Dict[str, str]
    base_vars: Dict[str, str]
    vars_list: Dict[str, List[str]]


class MakefileGenerator(ContentGeneratorBase):
    """Generates Makefile content with comprehensive build dependencies.

    This generator creates Makefile content that manages build dependencies
    for the accessibility guidelines documentation system. It processes
    various data sources including categories, check tools, FAQs, and info
    references to generate comprehensive dependency tracking.

    The generator integrates with multiple freee_a11y_gl models to collect
    dependency information and creates Makefile rules that ensure proper
    rebuild behavior when source files are modified. It supports complex
    dependency relationships and generates optimized build rules.

    Workflow:
        1. Initialize with language and configuration settings
        2. Collect base variables and source file paths
        3. Process all content types to gather dependencies
        4. Generate target rules with proper dependency tracking
        5. Combine all data into comprehensive Makefile content

    Attributes:
        config (MakefileConfig): Configuration settings for generation
        Inherits from ContentGeneratorBase:
        - lang (str): Language code for content generation
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> config = MakefileConfig(...)
        >>> generator = MakefileGenerator('ja', config)
        >>> for data in generator.generate():
        ...     print(f"Generated Makefile with "
        ...           f"{len(data['depends'])} dependencies")
    """

    def __init__(self, lang: str, config: MakefileConfig):
        """Initialize the Makefile generator with configuration.

        Sets up the generator with the specified language and configuration
        settings. The configuration provides all necessary parameters for
        Makefile generation including directory mappings and variable
        definitions.

        Args:
            lang (str): Language code for content generation
            config (MakefileConfig): Configuration settings for Makefile
                generation

        Example:
            >>> config = MakefileConfig(
            ...     dest_dirs={'guidelines': 'source/categories'},
            ...     makefile_vars={'LANG': 'ja'},
            ...     base_vars={'SRC_DIR': 'data/yaml'},
            ...     vars_list={'targets': ['all']}
            ... )
            >>> generator = MakefileGenerator('ja', config)
        """
        super().__init__(lang)
        self.config = config

    def generate(self):
        """Generate content for a single Makefile.

        Creates comprehensive Makefile content with build dependencies
        for the accessibility guidelines documentation system. The method
        processes all data sources to generate complete dependency tracking
        and build rules.

        Yields:
            Dict[str, Any]: Template data for Makefile generation

        Raises:
            Exception: If Makefile data generation fails

        Example:
            >>> generator = MakefileGenerator('ja', config)
            >>> data = next(generator.generate())
            >>> print(f"Generated Makefile with "
            ...       f"{len(data['depends'])} dependencies")
        """
        try:
            data = self.get_template_data()
            if data and self.validate_data(data):
                yield self.postprocess_data(data)
        except Exception as e:
            self.logger.error(
                f"Error generating makefile template data: {e}")
            raise

    def get_template_data(self) -> Dict[str, Any]:
        """Generate comprehensive Makefile data with all dependencies.

        Collects and processes all dependency information from various
        data sources to create complete Makefile content. This includes
        base variables, source file paths, target definitions, and
        dependency relationships for automated build management.

        Returns:
            Dict[str, Any]: Template data containing:
                - Base variables and configuration settings
                - Source file paths for all content types
                - Target definitions with dependency tracking
                - Build rules and dependency relationships

        Example:
            >>> generator = MakefileGenerator('ja', config)
            >>> data = generator.get_template_data()
            >>> print(f"Generated data with "
            ...       f"{len(data['depends'])} dependencies")
        """
        vars_data = self._prepare_base_variables()

        # Process all target types and collect dependencies
        all_dependencies, template_vars = self._collect_all_dependencies()

        # Combine all data
        result = {**vars_data, **self.config.makefile_vars,
                  **template_vars}
        result['depends'] = all_dependencies

        return result

    def _prepare_base_variables(self) -> Dict[str, Any]:
        """Prepare base makefile variables."""
        vars_data = self.config.base_vars.copy()

        # Set source YAML files
        vars_data.update({
            'check_yaml': ' '.join(Check.list_all_src_paths()),
            'gl_yaml': ' '.join(Guideline.list_all_src_paths()),
            'faq_yaml': ' '.join(Faq.list_all_src_paths())
        })

        return vars_data

    def _collect_all_dependencies(self) -> tuple[List[Dict[str, str]],
                                                 Dict[str, str]]:
        """Collect all build dependencies and template variables."""
        all_dependencies = []

        cat_deps, cat_targets = self._process_category_targets()
        check_deps, check_targets = self._process_checktool_targets()
        faq_deps, faq_article_targets, faq_tagpage_targets = (
            self._process_faq_targets())
        info_deps, info_to_gl_targets, info_to_faq_targets = (
            self._process_info_targets())

        # Collect all dependencies
        all_dependencies.extend(cat_deps)
        all_dependencies.extend(check_deps)
        all_dependencies.extend(faq_deps)
        all_dependencies.extend(info_deps)

        # Prepare template variables
        template_vars = {
            'guideline_category_target': ' '.join(cat_targets),
            'check_example_target': ' '.join(check_targets),
            'faq_article_target': ' '.join(faq_article_targets),
            'faq_tagpage_target': ' '.join(faq_tagpage_targets),
            'info_to_gl_target': ' '.join(info_to_gl_targets),
            'info_to_faq_target': ' '.join(info_to_faq_targets)
        }

        return all_dependencies, template_vars

    def _process_category_targets(self) -> tuple[List[Dict[str, str]],
                                                 List[str]]:
        """Process category targets and their dependencies."""
        build_depends = []
        category_targets = []
        for cat in Category.list_all():
            filename = f'{cat.id}.rst'
            target = os.path.join(self.config.dest_dirs['guidelines'],
                                  filename)
            if target not in category_targets:
                category_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(cat.get_dependency())
                })

        return build_depends, category_targets

    def _process_checktool_targets(self) -> tuple[List[Dict[str, str]],
                                                  List[str]]:
        """Process check tool targets and their dependencies."""
        build_depends = []
        checktool_targets = []

        for tool in CheckTool.list_all():
            filename = f'examples-{tool.id}.rst'
            target = os.path.join(self.config.dest_dirs['checks'],
                                  filename)
            if target not in checktool_targets:
                checktool_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(tool.get_dependency())
                })

        return build_depends, checktool_targets

    def _process_faq_targets(self) -> tuple[List[Dict[str, str]], List[str],
                                            List[str]]:
        """Process FAQ targets and their dependencies."""
        build_depends = []
        article_targets = []
        tagpage_targets = []

        # FAQ articles
        for faq in Faq.list_all():
            filename = f'{faq.id}.rst'
            target = os.path.join(self.config.dest_dirs['faq_articles'],
                                  filename)
            if target not in article_targets:
                article_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(faq.get_dependency())
                })

        # FAQ tag pages
        for tag in FaqTag.list_all():
            if tag.article_count() == 0:
                continue
            filename = f'{tag.id}.rst'
            target = os.path.join(self.config.dest_dirs['faq_tags'],
                                  filename)
            if target not in tagpage_targets:
                dependency = []
                tagpage_targets.append(target)
                for faq in self.relationship_manager.\
                        get_sorted_related_objects(tag, 'faq'):
                    dependency.extend(faq.get_dependency())
                build_depends.append({
                    'target': target,
                    'depends': ' '.join(dependency)
                })

        return build_depends, article_targets, tagpage_targets

    def _process_info_targets(self) -> tuple[List[Dict[str, str]], List[str],
                                             List[str]]:
        """Process info reference targets and their dependencies."""
        build_depends = []
        info_to_gl_targets = []
        info_to_faq_targets = []

        # Info to guidelines
        for info in InfoRef.list_has_guidelines():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.config.dest_dirs['info2gl'],
                                  filename)
            if target not in info_to_gl_targets:
                info_to_gl_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join([
                        guideline.src_path
                        for guideline in self.relationship_manager.
                        get_sorted_related_objects(info, 'guideline')
                    ])
                })

        # Info to FAQs
        for info in InfoRef.list_has_faqs():
            if not info.internal:
                continue
            filename = f'{info.ref}.rst'
            target = os.path.join(self.config.dest_dirs['info2faq'],
                                  filename)
            if target not in info_to_faq_targets:
                info_to_faq_targets.append(target)
                build_depends.append({
                    'target': target,
                    'depends': ' '.join([
                        faq.src_path
                        for faq in self.relationship_manager.
                        get_sorted_related_objects(info, 'faq')
                    ])
                })

        return build_depends, info_to_gl_targets, info_to_faq_targets

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate makefile data."""
        required_fields = ['depends', 'gl_yaml', 'check_yaml',
                           'faq_yaml']
        if not all(field in data for field in required_fields):
            return False

        if not isinstance(data['depends'], list):
            return False

        for dep in data['depends']:
            if (not isinstance(dep, dict) or 'target' not in dep or
                    'depends' not in dep):
                return False

        return True
