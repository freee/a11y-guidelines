"""Generators for miscellaneous definitions and reference content.

This module provides specialized generators for creating reference
documentation
from various data sources including InfoRef and AxeRule data. It supports the
creation of comprehensive reference materials for accessibility guidelines
documentation.

The module includes generators for:
- Info-to-guidelines reference pages linking information to related guidelines
- Info-to-FAQ reference pages connecting information to relevant FAQs
- Axe rules documentation for automated accessibility testing
- Miscellaneous definitions for external references

Classes:
    InfoToGuidelinesGenerator: Generates guideline reference pages from info
    InfoToFaqsGenerator: Generates FAQ reference pages from info
    AxeRulesGenerator: Generates axe rules documentation
    MiscDefinitionsGenerator: Generates miscellaneous definitions pages
"""
from typing import Dict, Any, List

from freee_a11y_gl import InfoRef, AxeRule
from ..content_generator_base import ContentGeneratorBase


class InfoToGuidelinesGenerator(ContentGeneratorBase):
    """Generates guideline reference pages from InfoRef data.

    This generator creates reference pages that link information references
    to their related accessibility guidelines. It processes internal InfoRef
    instances that have associated guidelines and creates documentation pages
    showing these relationships.

    The generator follows a list-based processing pattern, creating individual
    pages for each InfoRef that has guideline relationships. It uses the
    relationship manager to find and sort related guidelines, then formats
    them for template rendering.

    Workflow:
        1. Retrieve all internal InfoRef instances with guidelines
        2. Process each InfoRef individually
        3. Find related guidelines using relationship manager
        4. Format guideline data with category and ID information
        5. Generate filename and template data for each reference

    Attributes:
        Inherits from ContentGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = InfoToGuidelinesGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated reference for {data['filename']}")
    """

    def generate(self):
        """Generate content from a list of info references.

        Processes all internal InfoRef instances that have associated
        guidelines,
        creating reference pages that document the relationships between
        information references and accessibility guidelines.

        Yields:
            Dict[str, Any]: Template data for each info reference page

        Raises:
            Exception: If processing of any info reference fails

        Example:
            >>> generator = InfoToGuidelinesGenerator('ja')
            >>> pages = list(generator.generate())
            >>> print(f"Generated {len(pages)} reference pages")
        """
        items = self.get_items()
        self.logger.info(f"Processing {len(items)} info references")

        for item in items:
            try:
                data = self.process_item(item)
                if data and self.validate_data(data):
                    yield self.postprocess_data(data)
            except Exception as e:
                self.logger.error(
                    f"Error processing info reference {item}: {e}")
                raise

    def get_items(self) -> List[InfoRef]:
        """Get all internal info references that have associated guidelines.

        Retrieves InfoRef instances that are marked as internal and have
        relationships with accessibility guidelines. External references
        are excluded as they don't require local reference pages.

        Returns:
            List[InfoRef]: List of internal InfoRef instances with guidelines

        Example:
            >>> generator = InfoToGuidelinesGenerator('ja')
            >>> items = generator.get_items()
            >>> print(f"Found {len(items)} internal info references")
        """
        return [info for info in InfoRef.list_has_guidelines()
                if info.internal]

    def process_item(self, info: InfoRef) -> Dict[str, Any]:
        """Process a single info reference into template data.

        Transforms an InfoRef instance into the data structure required
        for template rendering. This includes generating the appropriate
        filename and extracting related guideline information formatted
        with category and ID data for the specified language.

        Args:
            info: InfoRef instance to process

        Returns:
            Dict[str, Any]: Template data containing:
                - filename (str): Reference identifier for the page
                - guidelines (List): Related guidelines with category and ID

        Example:
            >>> generator = InfoToGuidelinesGenerator('ja')
            >>> info = InfoRef.get_by_ref('wcag-sc')
            >>> data = generator.process_item(info)
            >>> print(f"Generated data for {data['filename']}")
        """
        guidelines = [
            guideline.get_category_and_id(self.lang)
            for guideline in self.relationship_manager.
            get_sorted_related_objects(info, 'guideline')
        ]
        return {
            'filename': info.ref,
            'guidelines': guidelines
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate guideline reference data structure.

        Ensures that the processed data contains all required fields
        for template rendering and that the guidelines field is properly
        formatted as a list. This validation prevents template errors
        and ensures data integrity.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'filename': 'wcag-sc', 'guidelines': [...]}
            >>> generator = InfoToGuidelinesGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return (self.validate_required_fields(
            data, ['filename', 'guidelines']) and
                isinstance(data['guidelines'], list))

    def get_dependencies(self) -> list[str]:
        """Get file dependencies for build system integration.

        Retrieves source file paths for all InfoRef instances that have
        guidelines to enable proper dependency tracking in the build system.
        This ensures that generated reference pages are rebuilt when source
        info files are modified.

        Returns:
            list[str]: List of source file paths for InfoRef instances

        Example:
            >>> generator = InfoToGuidelinesGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} info dependencies")
        """
        return [info.src_path for info in InfoRef.list_has_guidelines()]


class InfoToFaqsGenerator(ContentGeneratorBase):
    """Generates FAQ reference pages from InfoRef data.

    This generator creates reference pages that link information references
    to their related FAQ articles. It processes internal InfoRef instances
    that have associated FAQs and creates documentation pages showing these
    relationships for easy navigation and cross-referencing.

    The generator follows a list-based processing pattern, creating individual
    pages for each InfoRef that has FAQ relationships. It uses the
    relationship manager to find and sort related FAQs by their sort key,
    then formats them for template rendering.

    Workflow:
        1. Retrieve all internal InfoRef instances with FAQs
        2. Process each InfoRef individually
        3. Find related FAQs using relationship manager with sort_key
           ordering
        4. Extract FAQ IDs for template rendering
        5. Generate filename and template data for each reference

    Attributes:
        Inherits from ContentGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = InfoToFaqsGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated FAQ reference for {data['filename']}")
    """

    def generate(self):
        """Generate content from a list of info references.

        Processes all internal InfoRef instances that have associated FAQs,
        creating reference pages that document the relationships between
        information references and FAQ articles for improved navigation.

        Yields:
            Dict[str, Any]: Template data for each info reference page

        Raises:
            Exception: If processing of any info reference fails

        Example:
            >>> generator = InfoToFaqsGenerator('ja')
            >>> pages = list(generator.generate())
            >>> print(f"Generated {len(pages)} FAQ reference pages")
        """
        items = self.get_items()
        self.logger.info(f"Processing {len(items)} FAQ info references")

        for item in items:
            try:
                data = self.process_item(item)
                if data and self.validate_data(data):
                    yield self.postprocess_data(data)
            except Exception as e:
                self.logger.error(
                    f"Error processing FAQ info reference {item}: {e}")
                raise

    def get_items(self) -> List[InfoRef]:
        """Get all internal info references that have associated FAQs.

        Retrieves InfoRef instances that are marked as internal and have
        relationships with FAQ articles. External references are excluded
        as they don't require local reference pages.

        Returns:
            List[InfoRef]: List of internal InfoRef instances with FAQs

        Example:
            >>> generator = InfoToFaqsGenerator('ja')
            >>> items = generator.get_items()
            >>> print(f"Found {len(items)} internal info references "
            ...       f"with FAQs")
        """
        return [info for info in InfoRef.list_has_faqs() if info.internal]

    def process_item(self, info: InfoRef) -> Dict[str, Any]:
        """Process a single info reference into template data.

        Transforms an InfoRef instance into the data structure required
        for template rendering. This includes generating the appropriate
        filename and extracting related FAQ IDs sorted by their sort key
        for consistent ordering in the documentation.

        Args:
            info: InfoRef instance to process

        Returns:
            Dict[str, Any]: Template data containing:
                - filename (str): Reference identifier for the page
                - faqs (List[str]): Related FAQ IDs sorted by sort_key

        Example:
            >>> generator = InfoToFaqsGenerator('ja')
            >>> info = InfoRef.get_by_ref('accessibility-basics')
            >>> data = generator.process_item(info)
            >>> print(f"Generated data for {data['filename']} with "
            ...       f"{len(data['faqs'])} FAQs")
        """
        faqs = [
            faq.id
            for faq in self.relationship_manager.
            get_sorted_related_objects(info, 'faq', key='sort_key')
        ]
        return {
            'filename': info.ref,
            'faqs': faqs
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ reference data structure.

        Ensures that the processed data contains all required fields
        for template rendering and that the faqs field is properly
        formatted as a list. This validation prevents template errors
        and ensures data integrity.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'filename': 'accessibility-basics',
            ...         'faqs': ['p0001', 'p0002']}
            >>> generator = InfoToFaqsGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return (self.validate_required_fields(data, ['filename', 'faqs']) and
                isinstance(data['faqs'], list))

    def get_dependencies(self) -> list[str]:
        """Get file dependencies for build system integration.

        Retrieves source file paths for all InfoRef instances that have
        FAQs to enable proper dependency tracking in the build system.
        This ensures that generated reference pages are rebuilt when source
        info files are modified.

        Returns:
            list[str]: List of source file paths for InfoRef instances

        Example:
            >>> generator = InfoToFaqsGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} FAQ info dependencies")
        """
        return [info.src_path for info in InfoRef.list_has_faqs()]


class AxeRulesGenerator(ContentGeneratorBase):
    """Generates axe-core rules documentation.

    This generator creates comprehensive documentation for axe-core
    accessibility
    testing rules. It processes AxeRule data from the freee_a11y_gl library
    and formats it for template rendering, including version information,
    rule details, and metadata for automated accessibility testing reference.

    The generator follows the SingleFileGenerator pattern, producing one
    output file containing all axe-core rule information. It integrates
    with the AxeRule model to retrieve rule data and version metadata
    for comprehensive testing documentation.

    Workflow:
        1. Retrieve axe-core version and metadata information
        2. Get all available AxeRule instances
        3. Process each rule's template data for the specified language
        4. Combine version info and rule data for template rendering
        5. Validate and return formatted documentation data

    Attributes:
        Inherits from ContentGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = AxeRulesGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated docs for axe-core v{data['version']}")
    """

    def generate(self):
        """Generate content for axe-core rules documentation.

        Creates comprehensive documentation for axe-core accessibility testing
        rules, including version information and detailed rule specifications
        for automated testing reference.

        Yields:
            Dict[str, Any]: Template data for axe rules documentation

        Raises:
            Exception: If axe rules data generation fails

        Example:
            >>> generator = AxeRulesGenerator('ja')
            >>> data = next(generator.generate())
            >>> print(f"Generated {len(data['rules'])} axe rules")
        """
        try:
            data = self.get_template_data()
            if data and self.validate_data(data):
                yield self.postprocess_data(data)
        except Exception as e:
            self.logger.error(
                f"Error generating axe rules template data: {e}")
            raise

    def get_template_data(self) -> Dict[str, Any]:
        """Generate comprehensive axe-core rules data for template rendering.

        Retrieves axe-core version information and all available rules,
        formatting them for template processing. The method combines
        metadata (version, URL, timestamp) with detailed rule information
        to create complete testing documentation.

        Returns:
            Dict[str, Any]: Template data containing:
                - version (str): Full axe-core version string
                - major_version (str): Major version number
                - deque_url (str): Official Deque Systems URL
                - timestamp (str): Data generation timestamp
                - rules (List): Complete list of formatted rule data

        Example:
            >>> generator = AxeRulesGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(f"Generated data for axe-core v{data['version']}")
        """
        return {
            'version': AxeRule.version,
            'major_version': AxeRule.major_version,
            'deque_url': AxeRule.deque_url,
            'timestamp': AxeRule.timestamp,
            'rules': [rule.template_data(self.lang)
                      for rule in AxeRule.list_all()]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate axe-core rules data structure.

        Ensures that the generated data contains all required fields
        for template rendering, including version metadata and rules list.
        This validation prevents template rendering errors and ensures
        data integrity for axe-core documentation.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'version': '4.7.0', 'rules': [...], ...}
            >>> generator = AxeRulesGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        return (self.validate_required_fields(
            data, ['version', 'major_version', 'deque_url', 'timestamp',
                   'rules']) and isinstance(data['rules'], list))

    def get_dependencies(self) -> list[str]:
        """Get file dependencies for build system integration.

        Retrieves source file paths for all AxeRule instances to enable
        proper dependency tracking in the build system. This ensures that
        generated axe rules documentation is rebuilt when source rule
        files are modified.

        Returns:
            list[str]: List of source file paths for all axe rules

        Example:
            >>> generator = AxeRulesGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} axe rule dependencies")
        """
        return [rule.src_path for rule in AxeRule.list_all()]


class MiscDefinitionsGenerator(ContentGeneratorBase):
    """Generates miscellaneous definitions pages for external references.

    This generator creates documentation pages containing definitions and
    links for external references used throughout the accessibility
    guidelines. It processes external InfoRef instances and formats them
    into a comprehensive reference glossary with localized text and URLs.

    The generator follows the SingleFileGenerator pattern, producing one
    output file containing all external reference definitions. It integrates
    with InfoRef to retrieve external reference data and formats it for
    easy lookup and navigation.

    Workflow:
        1. Retrieve all external InfoRef instances
        2. Process each reference to extract link data
        3. Format reference information with labels, text, and URLs
        4. Combine all references into a unified definitions list
        5. Validate and return formatted definitions data

    Attributes:
        Inherits from ContentGeneratorBase:
        - lang (str): Language code for localized content
        - logger: Logging instance for operation tracking
        - relationship_manager: Access to object relationships

    Example:
        >>> generator = MiscDefinitionsGenerator('ja')
        >>> for data in generator.generate():
        ...     print(f"Generated {len(data['links'])} definitions")
    """

    def generate(self):
        """Generate content for miscellaneous definitions.

        Creates comprehensive definitions documentation for external
        references
        used throughout the accessibility guidelines, providing a centralized
        glossary with localized text and URLs for easy reference.

        Yields:
            Dict[str, Any]: Template data for definitions page

        Raises:
            Exception: If definitions data generation fails

        Example:
            >>> generator = MiscDefinitionsGenerator('ja')
            >>> data = next(generator.generate())
            >>> print(f"Generated {len(data['links'])} definitions")
        """
        try:
            data = self.get_template_data()
            if data and self.validate_data(data):
                yield self.postprocess_data(data)
        except Exception as e:
            self.logger.error(
                f"Error generating miscellaneous definitions "
                f"template data: {e}")
            raise

    def get_template_data(self) -> Dict[str, Any]:
        """Generate miscellaneous definitions data for template rendering.

        Retrieves all external InfoRef instances and processes them into
        a comprehensive definitions list. Each definition includes the
        reference label, localized text, and URL for the specified language.

        Returns:
            Dict[str, Any]: Template data containing:
                - links (List): Complete list of external reference
                  definitions

        Example:
            >>> generator = MiscDefinitionsGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(f"Generated {len(data['links'])} definitions")
        """
        data = []
        for info in InfoRef.list_all_external():
            link_data = info.link_data()
            data.append({
                'label': info.refstring(),
                'text': link_data['text'][self.lang],
                'url': link_data['url'][self.lang]
            })
        return {'links': data}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate miscellaneous definitions data structure.

        Ensures that the generated data contains the required 'links' field
        and that each link has the necessary label, text, and URL fields.
        This validation prevents template rendering errors and ensures
        data integrity for definitions documentation.

        Args:
            data: Template data dictionary to validate

        Returns:
            bool: True if data structure is valid, False otherwise

        Example:
            >>> data = {'links': [{'label': 'WCAG', 'text': '...',
            ...                    'url': '...'}]}
            >>> generator = MiscDefinitionsGenerator('ja')
            >>> is_valid = generator.validate_data(data)
            >>> print(f"Data is valid: {is_valid}")
        """
        if not self.validate_required_fields(data, ['links']):
            return False

        links = data['links']
        if not isinstance(links, list):
            return False

        for link in links:
            if not self.validate_required_fields(
                    link, ['label', 'text', 'url']):
                return False

        return True

    def get_dependencies(self) -> list[str]:
        """Get file dependencies for build system integration.

        Retrieves source file paths for all external InfoRef instances
        to enable proper dependency tracking in the build system. This
        ensures that generated definitions pages are rebuilt when source
        info files are modified.

        Returns:
            list[str]: List of source file paths for external InfoRef
                instances

        Example:
            >>> generator = MiscDefinitionsGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(f"Found {len(deps)} external info dependencies")
        """
        return [info.src_path for info in InfoRef.list_all_external()]
