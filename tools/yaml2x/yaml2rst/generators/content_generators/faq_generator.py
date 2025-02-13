"""Generators for FAQ-related content."""
from typing import Dict, Any, Iterator, List

from a11y_guidelines import Faq, FaqTag, RelationshipManager
from ..base_generator import BaseGenerator

class FaqArticleGenerator(BaseGenerator):
    """Generates individual FAQ article pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate FAQ article data.
        
        Yields:
            Dictionary containing FAQ article data
        """
        for faq in Faq.list_all():
            yield {'filename': faq.id, **faq.template_data(self.lang)}

    def get_dependencies(self) -> list[str]:
        return [faq.src_path for faq in Faq.list_all()]

class FaqTagPageGenerator(BaseGenerator):
    """Generates FAQ tag pages."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate FAQ tag page data.
        
        Yields:
            Dictionary containing tag page data with associated articles
        """
        rel = RelationshipManager()
        for tag in FaqTag.list_all():
            if tag.article_count() == 0:
                continue
            yield {
                'filename': tag.id,
                'tag': tag.id,
                'label': tag.names[self.lang],
                'articles': [faq.id for faq in rel.get_tag_to_faqs(tag)]
            }

    def get_dependencies(self) -> list[str]:
        return [faq.src_path for faq in Faq.list_all()]

class FaqIndexGenerator(BaseGenerator):
    """Generates the main FAQ index page."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate FAQ index data.
        
        Yields:
            Dictionary containing all tags and articles for the index
        """
        sorted_tags = sorted(FaqTag.list_all(), key=lambda x: x.names[self.lang])
        tags = [tag.template_data(self.lang) for tag in sorted_tags if tag.article_count() > 0]
        articles = [article.template_data(self.lang) for article in Faq.list_all(sort_by='date')]
        yield {'articles': articles, 'tags': tags}

    def get_dependencies(self) -> list[str]:
        return [faq.src_path for faq in Faq.list_all()]

class FaqTagIndexGenerator(BaseGenerator):
    """Generates the FAQ tag index page."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate FAQ tag index data.
        
        Yields:
            Dictionary containing all tags for the index
        """
        sorted_tags = sorted(FaqTag.list_all(), key=lambda x: x.names[self.lang])
        tagpages = [tagpage.template_data(self.lang) for tagpage in sorted_tags if tagpage.article_count() > 0]
        yield {'tags': tagpages}

    def get_dependencies(self) -> list[str]:
        return [faq.src_path for faq in Faq.list_all()]

class FaqArticleIndexGenerator(BaseGenerator):
    """Generates the FAQ article index page."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate FAQ article index data.
        
        Yields:
            Dictionary containing all articles for the index
        """
        articles = [article.template_data(self.lang) for article in Faq.list_all(sort_by='sortKey')]
        yield {'articles': articles}

    def get_dependencies(self) -> list[str]:
        return [faq.src_path for faq in Faq.list_all()]
