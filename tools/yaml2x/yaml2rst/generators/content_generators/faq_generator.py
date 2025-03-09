"""Generators for FAQ-related content."""
from typing import Dict, Any, List, Iterator

from freee_a11y_gl import Faq, FaqTag
from freee_a11y_gl.relationship_manager import RelationshipManager
from ..common_generators import SingleFileGenerator, ListBasedGenerator
from ..base_generator import BaseGenerator

class FaqGeneratorBase(BaseGenerator):
    """Base class for FAQ-related generators."""
    
    def __init__(self, lang: str):
        super().__init__(lang)
        self.relationship_manager = RelationshipManager()

    def get_dependencies(self) -> list[str]:
        """Get FAQ file dependencies."""
        return [faq.src_path for faq in Faq.list_all()]

    def get_sorted_tags(self) -> List[FaqTag]:
        """Get sorted list of tags with articles."""
        return sorted(
            [tag for tag in FaqTag.list_all() if tag.article_count() > 0],
            key=lambda x: x.names[self.lang]
        )

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ data."""
        return True  # 具体的なバリデーションは子クラスで実装

class FaqArticleGenerator(ListBasedGenerator[Faq], FaqGeneratorBase):
    """Generates individual FAQ article pages."""

    def get_items(self) -> List[Faq]:
        """Get all FAQ articles."""
        return Faq.list_all()

    def process_item(self, faq: Faq) -> Dict[str, Any]:
        """Process a single FAQ article."""
        return {
            'filename': faq.id,
            **faq.template_data(self.lang)
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FAQ article data."""
        required_fields = ['filename', 'title']
        return all(field in data for field in required_fields)

class FaqIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the main FAQ index page."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the index page data."""
        sorted_tags = self.get_sorted_tags()
        tags = [tag.template_data(self.lang) for tag in sorted_tags]
        articles = [article.template_data(self.lang) 
                   for article in Faq.list_all(sort_by='date')]
        return {
            'tags': tags,
            'articles': articles
        }

class FaqTagPageGenerator(ListBasedGenerator[FaqTag], FaqGeneratorBase):
    """Generates FAQ tag pages."""

    def get_items(self) -> List[FaqTag]:
        """Get all FAQ tags with articles."""
        return [tag for tag in FaqTag.list_all() if tag.article_count() > 0]

    def process_item(self, tag: FaqTag) -> Dict[str, Any]:
        """Process a single FAQ tag."""
        return {
            'filename': tag.id,
            'tag': tag.id,
            'label': tag.names[self.lang],
            'articles': [faq.id for faq in self.relationship_manager.get_tag_to_faqs(tag)]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate tag page data."""
        required_fields = ['filename', 'tag', 'label', 'articles']
        return all(field in data for field in required_fields)

class FaqTagIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the FAQ tag index page."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the tag index page data."""
        sorted_tags = self.get_sorted_tags()
        tagpages = [tag.template_data(self.lang) for tag in sorted_tags]
        return {'tags': tagpages}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate tag index data."""
        return 'tags' in data and isinstance(data['tags'], list)

class FaqArticleIndexGenerator(SingleFileGenerator, FaqGeneratorBase):
    """Generates the FAQ article index page."""

    def get_template_data(self) -> Dict[str, Any]:
        """Generate the article index page data."""
        articles = [article.template_data(self.lang) 
                   for article in Faq.list_all(sort_by='sortKey')]
        return {'articles': articles}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate article index data."""
        return 'articles' in data and isinstance(data['articles'], list)
