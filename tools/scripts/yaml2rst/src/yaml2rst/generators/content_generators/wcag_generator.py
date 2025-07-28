"""Generators for WCAG content.

This module provides specialized generators for creating WCAG (Web Content
Accessibility Guidelines) related documentation from YAML data sources.
It includes generators for WCAG mapping pages and priority difference
analysis, supporting comprehensive accessibility guidelines documentation.

The module integrates with the freee_a11y_gl library to access WCAG Success
Criteria data and provides generators for:
- WCAG mapping documentation showing relationships between guidelines and
  success criteria
- Priority difference analysis highlighting local vs. standard WCAG
  priorities
- Comprehensive error handling and validation

Classes:
    WcagGeneratorBase: Base functionality for WCAG-related generators
    WcagMappingGenerator: Generates WCAG mapping documentation
    PriorityDiffGenerator: Generates priority difference analysis
"""
from typing import Dict, Any, List

from freee_a11y_gl import WcagSc
from ..content_generator_base import ContentGeneratorBase
from ..common_generators import SingleFileGenerator


class WcagGeneratorBase(ContentGeneratorBase):
    """Base class for WCAG-related generators.

    This class provides common functionality for all WCAG-related content
    generators, including dependency management and guideline relationship
    processing. It serves as the foundation for specialized WCAG generators
    that process Web Content Accessibility Guidelines data.

    The class integrates with the freee_a11y_gl library to access WCAG
    Success Criteria data and provides standardized methods for dependency
    tracking and guideline relationship management.

    Attributes:
        Inherits all attributes from ContentGeneratorBase including:
        - lang (str): Language code for content generation
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> class CustomWcagGenerator(WcagGeneratorBase):
        ...     def get_template_data(self):
        ...         return {'wcag_data': WcagSc.get_all()}
        >>> generator = CustomWcagGenerator('ja')
        >>> dependencies = generator.get_dependencies()
    """

    def get_dependencies(self) -> list[str]:
        """Get WCAG Success Criteria file dependencies for build system
        integration.

        Retrieves all source file paths for WCAG Success Criteria data to
        enable proper dependency tracking in the build system. This ensures
        that generated content is rebuilt when source WCAG files are
        modified.

        Returns:
            list[str]: List of source file paths for all WCAG SC data files

        Example:
            >>> generator = WcagGeneratorBase('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} WCAG dependencies")
        """
        return [sc.src_path for sc in WcagSc.get_all().values()]

    def get_guidelines_for_sc(self, sc: WcagSc) -> List[Any]:
        """Get related guidelines for a WCAG Success Criterion.

        Retrieves and formats the guidelines that are related to a specific
        WCAG Success Criterion. The guidelines are sorted using the
        relationship manager and formatted with category and ID information
        for the specified language.

        Args:
            sc: WCAG Success Criterion to get guidelines for

        Returns:
            List[Any]: List of formatted guideline data with category and ID

        Example:
            >>> generator = WcagGeneratorBase('ja')
            >>> sc = WcagSc.get_by_id('1.1.1')
            >>> guidelines = generator.get_guidelines_for_sc(sc)
            >>> print(f"Found {len(guidelines)} related guidelines")
        """
        return [
            guideline.get_category_and_id(self.lang)
            for guideline in self.get_sorted_related_objects(sc, 'guideline')
        ]


class WcagMappingGenerator(SingleFileGenerator, WcagGeneratorBase):
    """Generates WCAG mapping documentation pages.

    This generator creates comprehensive mapping documentation that shows
    the relationships between WCAG Success Criteria and local accessibility
    guidelines. It processes all WCAG Success Criteria and their associated
    guidelines to create a unified mapping reference.

    The generator follows the SingleFileGenerator pattern, producing one
    output file containing all WCAG mapping information. It integrates
    with the WcagSc model to retrieve success criteria data and uses the
    relationship manager to find associated guidelines.

    Workflow:
        1. Retrieve all WCAG Success Criteria from WcagSc.get_all()
        2. For each success criterion, get template data
        3. Find related guidelines using get_guidelines_for_sc()
        4. Combine success criteria and guideline data
        5. Validate and return formatted mapping data

    Attributes:
        Inherits from SingleFileGenerator and WcagGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = WcagMappingGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated mapping for {len(data['mapping'])} "
        ...           f"criteria")
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate comprehensive WCAG mapping data for template rendering.

        Creates a complete mapping between WCAG Success Criteria and local
        accessibility guidelines. For each success criterion, the method
        retrieves the base template data and augments it with related
        guideline information when available.

        Returns:
            Dict[str, Any]: Template data containing:
                - mapping (List): Complete list of WCAG SC with related
                  guidelines

        Example:
            >>> generator = WcagMappingGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(f"Generated mapping for {len(data['mapping'])} "
            ...       f"criteria")
        """
        mappings = []
        for sc in WcagSc.get_all().values():
            sc_object = sc.template_data()
            guidelines = self.get_guidelines_for_sc(sc)
            if guidelines:
                sc_object['guidelines'] = guidelines
            mappings.append(sc_object)
        return {'mapping': mappings}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate WCAG mapping data structure.

        Ensures that the generated data contains the required 'mapping'
        field and that it is properly formatted as a list. This validation
        prevents template rendering errors and ensures data integrity.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'mapping': [{'id': '1.1.1', 'guidelines': [...]}]}
            >>> generator = WcagMappingGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return self.validate_list_field(data, 'mapping')


class PriorityDiffGenerator(SingleFileGenerator, WcagGeneratorBase):
    """Generates priority difference analysis pages.

    This generator creates documentation highlighting differences between
    standard WCAG priority levels and local priority assignments. It
    identifies success criteria where the local priority differs from the
    standard WCAG level, providing transparency about priority
    customizations.

    The generator follows the SingleFileGenerator pattern, producing one
    output file containing all priority difference information. It filters
    WCAG Success Criteria to include only those with priority differences
    and formats them for documentation.

    Workflow:
        1. Retrieve all WCAG Success Criteria from WcagSc.get_all()
        2. Filter criteria where sc.level != sc.local_priority
        3. Generate template data for filtered criteria
        4. Validate and return formatted difference data

    Attributes:
        Inherits from SingleFileGenerator and WcagGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = PriorityDiffGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Found {len(data['diffs'])} priority differences")
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate priority difference data for template rendering.

        Identifies and formats WCAG Success Criteria that have different
        local priority assignments compared to their standard WCAG levels.
        This analysis helps document and explain priority customizations
        made for local accessibility requirements.

        Returns:
            Dict[str, Any]: Template data containing:
                - diffs (List): Success criteria with priority differences

        Example:
            >>> generator = PriorityDiffGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(f"Found {len(data['diffs'])} priority differences")
        """
        diffs = [
            sc.template_data()
            for sc in WcagSc.get_all().values()
            if sc.level != sc.local_priority
        ]
        return {'diffs': diffs}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate priority difference data structure.

        Ensures that the generated data contains the required 'diffs'
        field and that it is properly formatted as a list. This validation
        prevents template rendering errors and ensures data integrity.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'diffs': [{'id': '1.1.1', 'level': 'A',
            ...                   'local_priority': 'AA'}]}
            >>> generator = PriorityDiffGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return self.validate_list_field(data, 'diffs')
