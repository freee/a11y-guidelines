"""Generator for guideline category pages.

This module provides the CategoryGenerator class for creating RST documentation
pages for guideline categories. Each category page contains associated
guidelines organized and formatted for accessibility documentation.

The generator processes category data from the freee_a11y_gl library and
creates individual RST files for each category, including proper
cross-references and navigation structure.
"""
from typing import Dict, Any, Iterator, List

from freee_a11y_gl import Category
from ..content_generator_base import ContentGeneratorBase


class CategoryGenerator(ContentGeneratorBase):
    """Generates RST pages for guideline categories with associated guidelines.

    The CategoryGenerator creates individual category pages that display
    guidelines organized by category. Each page includes the category
    information and all guidelines that belong to that category, formatted
    for RST documentation generation.

    The generator uses the freee_a11y_gl library to access category and
    guideline data, and leverages the RelationshipManager to find associated
    guidelines for each category.

    Workflow:
        1. Load all available categories from the data source
        2. For each category, retrieve associated guidelines
        3. Process category and guideline data for template rendering
        4. Generate RST content using the category_page template
        5. Validate and yield processed data for file writing

    Attributes:
        categories_by_id (Dict[str, Category]): Mapping of category IDs to
            Category objects

    Example:
        >>> generator = CategoryGenerator('ja')
        >>> for category_data in generator.generate():
        ...     print(f"Generated category: {category_data['filename']}")
        Generated category: form
        Generated category: image
        Generated category: text
    """

    def __init__(self, lang: str):
        """Initialize the category generator for a specific language.

        Sets up the generator with the target language and creates a mapping
        of category IDs to Category objects for efficient lookup during
        the generation process.

        Args:
            lang: Target language code (e.g., 'ja', 'en')

        Example:
            >>> generator = CategoryGenerator('ja')
            >>> print(len(generator.categories_by_id))  # Number of categories
        """
        super().__init__(lang)
        self.categories_by_id = {cat.id: cat for cat in Category.list_all()}

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate content from a list of category IDs.

        Processes all available categories and yields template data for each
        category page. The method handles error logging and data validation
        to ensure robust generation.

        Yields:
            Template data dictionaries for category pages, each containing:
            - filename: Category ID used as the output filename
            - guidelines: List of guideline template data for the category

        Raises:
            Exception: Re-raises any processing errors after logging

        Example:
            >>> generator = CategoryGenerator('ja')
            >>> for data in generator.generate():
            ...     template_manager.write_rst(data, f"{data['filename']}.rst")
        """
        items = self.get_items()
        self.logger.info(f"Processing {len(items)} categories")

        for item in items:
            try:
                data = self.process_item(item)
                if data and self.validate_data(data):
                    yield self.postprocess_data(data)
            except Exception as e:
                self.logger.error(f"Error processing category {item}: {e}")
                raise

    def get_items(self) -> List[str]:
        """Get all category IDs to process.

        Returns a list of all available category IDs that should be
        processed for page generation. This method provides the complete
        list of categories from the loaded data.

        Returns:
            List of category ID strings

        Example:
            >>> generator = CategoryGenerator('ja')
            >>> items = generator.get_items()
            >>> print(items)  # ['form', 'image', 'text', 'multimedia', ...]
        """
        return list(self.categories_by_id.keys())

    def process_item(self, category_id: str) -> Dict[str, Any]:
        """Process a single category into template data.

        Takes a category ID and processes it into the data structure needed
        for template rendering. This includes retrieving the category object,
        finding associated guidelines, and formatting the data appropriately.

        Args:
            category_id: The ID of the category to process

        Returns:
            Dictionary containing template data:
            - filename: Category ID for output filename
            - guidelines: List of guideline template data dictionaries

        The guidelines are sorted according to the RelationshipManager's
        sorting logic and converted to template data format for the
        specified language.

        Example:
            >>> generator = CategoryGenerator('ja')
            >>> data = generator.process_item('form')
            >>> print(data['filename'])  # 'form'
            >>> print(len(data['guidelines']))  # Number of form guidelines
        """
        category = self.categories_by_id[category_id]
        guidelines = self.relationship_manager.get_sorted_related_objects(
            category, 'guideline')
        return {
            'filename': category_id,
            'guidelines': [gl.template_data(self.lang) for gl in guidelines]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate category page data structure.

        Ensures that the processed category data contains all required
        fields and that the data types are correct for template rendering.

        Args:
            data: The processed category data to validate

        Returns:
            True if data is valid, False otherwise

        Validation checks:
        - Required fields 'filename' and 'guidelines' are present
        - 'guidelines' field is a list (may be empty)

        Example:
            >>> data = {'filename': 'form', 'guidelines': []}
            >>> generator = CategoryGenerator('ja')
            >>> is_valid = generator.validate_data(data)  # True
            >>>
            >>> invalid_data = {'filename': 'form'}  # Missing guidelines
            >>> is_valid = generator.validate_data(invalid_data)  # False
        """
        return (self.validate_required_fields(data, ['filename', 'guidelines'])
                and isinstance(data['guidelines'], list))

    def get_dependencies(self) -> List[str]:
        """Get category file dependencies for build system integration.

        Returns a list of file dependencies that should trigger regeneration
        of category pages when modified. This is used by the build system
        to determine when category pages need to be rebuilt.

        Returns:
            List of dependency file paths for all categories

        The dependencies include the source files that define each category,
        which are typically YAML files in the data directory structure.

        Example:
            >>> generator = CategoryGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(deps[0])  # Path to first category dependency file
        """
        return [cat.get_dependency() for cat in Category.list_all()]
