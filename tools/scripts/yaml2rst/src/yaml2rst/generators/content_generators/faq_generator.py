"""Generators for FAQ-related content.

This module provides a comprehensive set of generators for creating FAQ
(Frequently Asked Questions) documentation in various formats. It includes
generators for individual FAQ articles, tag-based organization pages,
and index pages for navigation.

The FAQ system supports:
- Individual FAQ article pages with full content
- Tag-based categorization and filtering
- Multiple index pages for different navigation patterns
- Cross-references between FAQs and tags

Classes:
    FaqGeneratorBase: Base class providing common FAQ functionality
    FaqArticleGenerator: Generates individual FAQ article pages
    FaqIndexGenerator: Generates the main FAQ index page
    FaqTagPageGenerator: Generates pages for FAQ tags with associated articles
    FaqTagIndexGenerator: Generates index of all FAQ tags
    FaqArticleIndexGenerator: Generates index of all FAQ articles
"""
from typing import Dict, Any, List

from freee_a11y_gl import Faq, FaqTag
from ..common_generators import SingleFileGenerator, ListBasedGenerator
from ..content_generator_base import ContentGeneratorBase


class FaqGeneratorBase(ContentGeneratorBase):
    """Base class for FAQ-related generators.

    Provides common functionality shared across all FAQ generators,
    including dependency management, tag sorting, and basic validation.
    This base class consolidates FAQ-specific operations to avoid
    code duplication across the various FAQ generator types.

    Common Features:
    - FAQ file dependency tracking for build system integration
    - Tag sorting with article count filtering
    - Base validation framework for FAQ data structures

    This class should not be instantiated directly; use one of the
    concrete FAQ generator classes instead.
    """

    def get_dependencies(self) -> List[str]:
        """Get FAQ file dependencies for build system integration.

        Returns a list of source file paths that should trigger regeneration
        of FAQ content when modified. This includes all FAQ YAML files
        in the data directory structure.

        Returns:
            List of FAQ source file paths

        Example:
            >>> generator = FaqArticleGenerator('ja')
            >>> deps = generator.get_dependencies()
            >>> print(deps[0])  # '/data/yaml/faq/p0001.yaml'
        """
        return [faq.src_path for faq in Faq.list_all()]

    def get_sorted_tags(self) -> List[FaqTag]:
        """Get sorted list of FAQ tags that have associated articles.

        Filters FAQ tags to include only those with at least one associated
        article, then sorts them by localized name for the target language.
        This ensures that empty tags are not included in navigation.

        Returns:
            List of FaqTag objects sorted by localized name

        Example:
            >>> generator = FaqArticleGenerator('ja')
            >>> tags = generator.get_sorted_tags()
            >>> print([tag.names['ja'] for tag in tags])
            # ['デザイン', 'プロダクト']
        """
        tags_with_articles = self.filter_objects_with_articles(
            FaqTag.list_all())
        return self.get_sorted_objects_by_lang_name(
            tags_with_articles, self.lang)

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ data structure.

        Base validation method that can be overridden by subclasses
        for specific validation requirements. The base implementation
        always returns True, allowing subclasses to implement their
        own validation logic.

        Args:
            data: The FAQ data dictionary to validate

        Returns:
            True if data is valid, False otherwise

        Note:
            Concrete FAQ generator classes should override this method
            to implement specific validation rules for their data structures.
        """
        return True  # Specific validation implemented in subclasses


class FaqArticleGenerator(ListBasedGenerator[Faq], FaqGeneratorBase):
    """Generates individual FAQ article pages.

    Creates separate RST files for each FAQ article, containing the full
    article content including title, body text, tags, and metadata.
    Each article is rendered using the faq_article template.

    The generator processes all available FAQ articles and creates
    individual pages that can be cross-referenced from tag pages
    and index pages.

    Output:
        Individual .rst files named by FAQ ID (e.g., p0001.rst, d0002.rst)

    Example:
        >>> generator = FaqArticleGenerator('ja')
        >>> for article_data in generator.generate():
        ...     print(f"Generated FAQ: {article_data['filename']}")
        Generated FAQ: p0001
        Generated FAQ: p0002
        Generated FAQ: d0001
    """

    def get_items(self) -> List[Faq]:
        """Get all FAQ articles to process.

        Returns the complete list of FAQ articles available in the
        data source. All articles are processed regardless of their
        tag associations or other metadata.

        Returns:
            List of all Faq objects

        Example:
            >>> generator = FaqArticleGenerator('ja')
            >>> faqs = generator.get_items()
            >>> print(len(faqs))  # Total number of FAQ articles
        """
        return Faq.list_all()

    def process_item(self, faq: Faq) -> Dict[str, Any]:
        """Process a single FAQ article into template data.

        Converts a Faq object into the data structure needed for
        template rendering. This includes the filename for output
        and all template data from the FAQ object.

        Args:
            faq: The Faq object to process

        Returns:
            Dictionary containing:
            - filename: FAQ ID for output filename
            - All template data from faq.template_data()

        The template data includes localized title, content, tags,
        and other metadata formatted for the target language.

        Example:
            >>> generator = FaqArticleGenerator('ja')
            >>> faq = Faq.get('p0001')
            >>> data = generator.process_item(faq)
            >>> print(data['filename'])  # 'p0001'
            >>> print(data['title'])  # Japanese title
        """
        return {
            'filename': faq.id,
            **faq.template_data(self.lang)
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ article data structure.

        Ensures that the processed FAQ article data contains all
        required fields for template rendering.

        Args:
            data: The processed FAQ article data to validate

        Returns:
            True if data is valid, False otherwise

        Validation checks:
        - Required fields 'filename' and 'title' are present

        Example:
            >>> data = {'filename': 'p0001', 'title': 'FAQ Title'}
            >>> generator = FaqArticleGenerator('ja')
            >>> is_valid = generator.validate_data(data)  # True
        """
        required_fields = ['filename', 'title']
        return self.validate_required_fields(data, required_fields)


class FaqIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the main FAQ index page.

    Creates a single index page that provides navigation to all FAQ
    content, including both tag-based navigation and a complete
    article listing. This serves as the main entry point for FAQ
    documentation.

    The index page includes:
    - List of all FAQ tags with article counts
    - Complete list of FAQ articles sorted by date
    - Navigation links to tag pages and individual articles

    Output:
        Single index.rst file for FAQ navigation

    Example:
        >>> generator = FaqIndexGenerator('ja')
        >>> data = generator.get_template_data()
        >>> print(len(data['tags']))  # Number of tags with articles
        >>> print(len(data['articles']))  # Total number of articles
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the FAQ index page template data.

        Creates the data structure needed for rendering the main FAQ
        index page, including sorted tags and articles.

        Returns:
            Dictionary containing:
            - tags: List of tag template data for navigation
            - articles: List of article template data sorted by date

        The tags are filtered to include only those with articles
        and sorted by localized name. Articles are sorted by date
        to show the most recent content first.

        Example:
            >>> generator = FaqIndexGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(data['tags'][0]['name'])  # First tag name
            >>> print(data['articles'][0]['title'])
            # Most recent article title
        """
        sorted_tags = self.get_sorted_tags()
        tags = [tag.template_data(self.lang) for tag in sorted_tags]
        articles = [article.template_data(self.lang)
                    for article in Faq.list_all(sort_by='date')]
        return {
            'tags': tags,
            'articles': articles
        }


class FaqTagPageGenerator(ListBasedGenerator[FaqTag], FaqGeneratorBase):
    """Generates FAQ tag pages with associated articles.

    Creates individual pages for each FAQ tag that has associated
    articles. Each tag page lists all articles tagged with that
    specific tag, providing topic-based navigation through FAQ content.

    Tag pages include:
    - Tag name and description
    - List of all articles with that tag
    - Links to individual article pages

    Output:
        Individual .rst files for each tag (e.g., design.rst, product.rst)

    Example:
        >>> generator = FaqTagPageGenerator('ja')
        >>> for tag_data in generator.generate():
        ...     print(f"Generated tag page: {tag_data['filename']}")
        Generated tag page: design
        Generated tag page: product
    """

    def get_items(self) -> List[FaqTag]:
        """Get all FAQ tags that have associated articles.

        Filters FAQ tags to include only those with at least one
        associated article. Empty tags are excluded from page generation.

        Returns:
            List of FaqTag objects that have articles

        Example:
            >>> generator = FaqTagPageGenerator('ja')
            >>> tags = generator.get_items()
            >>> all(tag.article_count() > 0 for tag in tags)  # True
        """
        return [tag for tag in FaqTag.list_all()
                if tag.article_count() > 0]

    def process_item(self, tag: FaqTag) -> Dict[str, Any]:
        """Process a single FAQ tag into template data.

        Converts a FaqTag object into the data structure needed for
        template rendering, including the tag information and list
        of associated article IDs.

        Args:
            tag: The FaqTag object to process

        Returns:
            Dictionary containing:
            - filename: Tag ID for output filename
            - tag: Tag ID for template reference
            - label: Localized tag name
            - articles: List of article IDs associated with this tag

        Articles are sorted according to the RelationshipManager's
        sorting logic to ensure consistent ordering.

        Example:
            >>> generator = FaqTagPageGenerator('ja')
            >>> tag = FaqTag.get('design')
            >>> data = generator.process_item(tag)
            >>> print(data['filename'])  # 'design'
            >>> print(data['label'])  # 'デザイン'
            >>> print(data['articles'])  # ['d0001', 'd0002', ...]
        """
        return {
            'filename': tag.id,
            'tag': tag.id,
            'label': tag.names[self.lang],
            'articles': [faq.id for faq in
                         self.relationship_manager.get_sorted_related_objects(
                             tag, 'faq', key='sort_key')]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ tag page data structure.

        Ensures that the processed tag page data contains all required
        fields and that the data types are correct for template rendering.

        Args:
            data: The processed tag page data to validate

        Returns:
            True if data is valid, False otherwise

        Validation checks:
        - Required fields 'filename', 'tag', 'label', 'articles' are present
        - 'articles' field is a list

        Example:
            >>> data = {
            ...     'filename': 'design',
            ...     'tag': 'design',
            ...     'label': 'デザイン',
            ...     'articles': ['d0001', 'd0002']
            ... }
            >>> generator = FaqTagPageGenerator('ja')
            >>> is_valid = generator.validate_data(data)  # True
        """
        required_fields = ['filename', 'tag', 'label', 'articles']
        return (self.validate_required_fields(data, required_fields) and
                self.validate_list_field(data, 'articles'))


class FaqTagIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the FAQ tag index page.

    Creates a single index page that lists all FAQ tags with associated
    articles. This provides an overview of all available topic categories
    and serves as a navigation hub for tag-based browsing.

    The tag index includes:
    - Complete list of tags with article counts
    - Links to individual tag pages
    - Alphabetical sorting by localized tag names

    Output:
        Single tag_index.rst file for tag navigation

    Example:
        >>> generator = FaqTagIndexGenerator('ja')
        >>> data = generator.get_template_data()
        >>> print(len(data['tags']))  # Number of tags with articles
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the FAQ tag index page template data.

        Creates the data structure needed for rendering the tag index
        page, including all tags that have associated articles.

        Returns:
            Dictionary containing:
            - tags: List of tag template data sorted by localized name

        Only tags with at least one article are included in the index.

        Example:
            >>> generator = FaqTagIndexGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(data['tags'][0]['name'])  # First tag name
            >>> print(data['tags'][0]['article_count'])
            # Number of articles
        """
        sorted_tags = self.get_sorted_tags()
        tagpages = [tag.template_data(self.lang) for tag in sorted_tags]
        return {'tags': tagpages}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ tag index data structure.

        Ensures that the tag index data contains the required tags list
        and that it is properly formatted as a list.

        Args:
            data: The tag index data to validate

        Returns:
            True if data is valid, False otherwise

        Validation checks:
        - 'tags' field exists and is a list

        Example:
            >>> data = {'tags': [{'name': 'Design', 'id': 'design'}]}
            >>> generator = FaqTagIndexGenerator('ja')
            >>> is_valid = generator.validate_data(data)  # True
        """
        return self.validate_list_field(data, 'tags')


class FaqArticleIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the FAQ article index page.

    Creates a single index page that lists all FAQ articles in a
    comprehensive format. This provides an alternative navigation
    method to the tag-based approach, showing all articles in
    a single sorted list.

    The article index includes:
    - Complete list of all FAQ articles
    - Sorting by article sort key for consistent ordering
    - Links to individual article pages
    - Article metadata for quick reference

    Output:
        Single article_index.rst file for article navigation

    Example:
        >>> generator = FaqArticleIndexGenerator('ja')
        >>> data = generator.get_template_data()
        >>> print(len(data['articles']))  # Total number of articles
    """

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the FAQ article index page template data.

        Creates the data structure needed for rendering the article index
        page, including all available FAQ articles sorted by sort key.

        Returns:
            Dictionary containing:
            - articles: List of article template data sorted by sortKey

        Articles are sorted by their sortKey attribute to ensure
        consistent and logical ordering in the index.

        Example:
            >>> generator = FaqArticleIndexGenerator('ja')
            >>> data = generator.get_template_data()
            >>> print(data['articles'][0]['title'])  # First article title
            >>> print(data['articles'][0]['id'])  # First article ID
        """
        articles = [article.template_data(self.lang)
                    for article in Faq.list_all(sort_by='sortKey')]
        return {'articles': articles}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ article index data structure.

        Ensures that the article index data contains the required articles
        list and that it is properly formatted as a list.

        Args:
            data: The article index data to validate

        Returns:
            True if data is valid, False otherwise

        Validation checks:
        - 'articles' field exists and is a list

        Example:
            >>> data = {'articles': [{'title': 'FAQ 1', 'id': 'p0001'}]}
            >>> generator = FaqArticleIndexGenerator('ja')
            >>> is_valid = generator.validate_data(data)  # True
        """
        return self.validate_list_field(data, 'articles')
