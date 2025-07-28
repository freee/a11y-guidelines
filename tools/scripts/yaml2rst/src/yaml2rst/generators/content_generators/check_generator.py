"""Generators for check-related content.

This module provides specialized generators for creating check-related
documentation from YAML data sources. It includes generators for comprehensive
check listings and individual check tool examples, supporting the accessibility
guidelines documentation system.

The module follows the established generator architecture with:
- Base classes providing common functionality
- Mixin integration for relationship management and validation
- Comprehensive error handling and logging
- Type-safe data processing with validation

Classes:
    CheckGeneratorBase: Base functionality for check-related generators
    AllChecksGenerator: Generates comprehensive check listings
    CheckExampleGenerator: Generates individual check tool example pages
"""
from typing import Dict, Any, List

from freee_a11y_gl import Check, CheckTool
from ..common_generators import SingleFileGenerator, ListBasedGenerator
from ..content_generator_base import ContentGeneratorBase


class CheckGeneratorBase(ContentGeneratorBase):
    """Base class for check-related generators.

    This class provides common functionality for all check-related content
    generators, including dependency management and basic validation. It serves
    as the foundation for specialized check generators that process
    accessibility check data.

    The class integrates with the freee_a11y_gl library to access check data
    and
    provides standardized methods for dependency tracking and data validation.

    Attributes:
        Inherits all attributes from ContentGeneratorBase including:
        - lang (str): Language code for content generation
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> class CustomCheckGenerator(CheckGeneratorBase):
        ...     def get_template_data(self):
        ...         return {'checks': Check.list_all()}
        >>> generator = CustomCheckGenerator('ja')
        >>> dependencies = generator.get_dependencies()
    """

    def get_dependencies(self) -> list[str]:
        """Get check file dependencies for build system integration.

        Retrieves all source file paths for check data to enable proper
        dependency tracking in the build system. This ensures that generated
        content is rebuilt when source check files are modified.

        Returns:
            list[str]: List of source file paths for all check data files

        Example:
            >>> generator = CheckGeneratorBase('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} check dependencies")
        """
        return Check.list_all_src_paths()

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate check data structure.

        Provides basic validation for check-related data. Subclasses should
        override this method to implement specific validation logic for their
        data structures.

        Args:
            data: Data dictionary to validate

        Returns:
            bool: True if data is valid, False otherwise

        Note:
            This base implementation always returns True. Subclasses should
            provide meaningful validation logic.
        """
        return True


class AllChecksGenerator(SingleFileGenerator, CheckGeneratorBase):
    """Generates comprehensive check listings for accessibility guidelines.

    This generator creates a single page containing all accessibility checks
    organized and formatted for documentation. It processes check data from
    the freee_a11y_gl library and formats it for template rendering.

    The generator follows the SingleFileGenerator pattern, producing one
    output file containing all check information. It integrates with the
    Check model to retrieve and format check data according to the specified
    language requirements.

    Workflow:
        1. Retrieve all check data using Check.template_data_all()
        2. Convert generator output to list for template processing
        3. Validate the resulting data structure
        4. Return formatted data for template rendering

    Attributes:
        Inherits from SingleFileGenerator and CheckGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = AllChecksGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated {len(data['allchecks'])} checks")
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate comprehensive check data for template rendering.

        Retrieves all accessibility check data from the freee_a11y_gl library
        and formats it for template processing. The method converts the
        generator output to a list to ensure compatibility with template
        systems that require indexable collections.

        Returns:
            Dict[str, Any]: Template data containing:
                - allchecks (List): Complete list of formatted check data

        Raises:
            Exception: If check data retrieval or processing fails

        Example:
            >>> generator = AllChecksGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(f"Retrieved {len(data['allchecks'])} checks")
        """
        self.logger.info("Generating all checks data")
        allchecks = list(Check.template_data_all(self.lang))  # ジェネレーターをリストに変換
        self.logger.info(f"Generated {len(allchecks)} checks")
        return {'allchecks': allchecks}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate all checks data structure.

        Ensures that the generated data contains the required 'allchecks'
        field and that it is properly formatted as a list. This validation
        prevents template rendering errors and ensures data integrity.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'allchecks': [{'id': 'check1'}, {'id': 'check2'}]}
            >>> generator = AllChecksGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return self.validate_list_field(data, 'allchecks')


class CheckExampleGenerator(ListBasedGenerator[CheckTool], CheckGeneratorBase):
    """Generates individual check tool example pages.

    This generator creates separate documentation pages for each check tool,
    containing detailed examples and usage information. It follows the
    ListBasedGenerator pattern to process each CheckTool individually,
    creating focused documentation for specific accessibility checking tools.

    The generator integrates with the CheckTool model from freee_a11y_gl
    to retrieve tool-specific example data and formats it for template
    rendering. Each generated page provides comprehensive examples showing
    how to use the specific check tool effectively.

    Workflow:
        1. Retrieve all available CheckTool instances
        2. Process each tool individually to extract example data
        3. Generate filename and template data for each tool
        4. Validate the resulting data structure
        5. Yield formatted data for template rendering

    Attributes:
        Inherits from ListBasedGenerator[CheckTool] and CheckGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = CheckExampleGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated examples for {data['filename']}")
    """

    def get_items(self) -> List[CheckTool]:
        """Get all available check tools for processing.

        Retrieves the complete list of CheckTool instances from the
        freee_a11y_gl library. Each tool represents a specific accessibility
        checking utility with associated examples and documentation.

        Returns:
            List[CheckTool]: Complete list of available check tools

        Example:
            >>> generator = CheckExampleGenerator('ja')
            >>> tools = generator.get_items()
            >>> print(f"Found {len(tools)} check tools")
        """
        return CheckTool.list_all()

    def process_item(self, tool: CheckTool) -> Dict[str, Any]:
        """Process a single check tool into template data.

        Transforms a CheckTool instance into the data structure required
        for template rendering. This includes generating the appropriate
        filename and extracting localized example data for the tool.

        Args:
            tool: CheckTool instance to process

        Returns:
            Dict[str, Any]: Template data containing:
                - filename (str): Generated filename for the tool's page
                - examples: Localized example data for the tool

        Example:
            >>> generator = CheckExampleGenerator('ja')
            >>> tool = CheckTool.get_by_id('axe-core')
            >>> data = generator.process_item(tool)
            >>> print(f"Generated data for {data['filename']}")
        """
        return {
            'filename': f'examples-{tool.id}',
            'examples': tool.example_template_data(self.lang)
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate check example data structure.

        Ensures that the processed data contains all required fields
        for template rendering. This validation prevents template errors
        and ensures data integrity for check tool example pages.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'filename': 'examples-axe', 'examples': [...]}
            >>> generator = CheckExampleGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        required_fields = ['filename', 'examples']
        return self.validate_required_fields(data, required_fields)

    def get_dependencies(self) -> list[str]:
        """Get check tool file dependencies for build system integration.

        Retrieves source file paths for all check tools to enable proper
        dependency tracking in the build system. This ensures that generated
        example pages are rebuilt when source tool files are modified.

        Returns:
            list[str]: List of source file paths for all check tools

        Example:
            >>> generator = CheckExampleGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} tool dependencies")
        """
        return [tool.src_path for tool in CheckTool.list_all()]
