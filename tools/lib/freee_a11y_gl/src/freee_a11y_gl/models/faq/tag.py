"""FAQ tag model for categorizing FAQ articles."""
from typing import Dict, List, Optional, Any
from ..base import BaseModel


class FaqTag(BaseModel):
    """Tag for categorizing FAQ articles."""

    object_type = "faq_tag"
    _instances: Dict[str, 'FaqTag'] = {}

    def __init__(self, tag_id: str, names: Dict[str, str]):
        """Initialize FAQ tag.

        Args:
            tag_id: Tag identifier
            names: Dictionary of localized tag names
        """
        super().__init__(tag_id)
        self.names = names
        FaqTag._instances[tag_id] = self

    def article_count(self) -> int:
        """Get number of articles with this tag."""
        rel = self._get_relationship_manager()
        return len(rel.get_related_objects(self, 'faq'))

    def get_name(self, lang: str) -> str:
        """Get localized tag name.

        Args:
            lang: Language code

        Returns:
            Localized name, falls back to English
        """
        return self.names.get(lang, self.names['en'])

    def template_data(self, lang: str) -> Optional[Dict[str, Any]]:
        """Get template data for tag.

        Args:
            lang: Language code

        Returns:
            Dictionary with tag data or None if tag has no articles
        """
        rel = self._get_relationship_manager()
        faqs = rel.get_related_objects(self, 'faq')
        if not faqs:
            return None

        sorted_faqs = sorted(faqs, key=lambda x: x.sort_key)
        return {
            'tag': self.id,
            'label': self.names[lang],
            'articles': [faq.id for faq in sorted_faqs],
            'count': len(faqs)
        }

    @classmethod
    def list_all(cls, **kwargs) -> List['FaqTag']:
        """Get all tags, optionally sorted.

        Args:
            **kwargs: Optional sorting parameters:
                - sort_by: One of 'count', 'label'

        Returns:
            List of tag instances
        """
        if 'sort_by' in kwargs:
            if kwargs['sort_by'] == 'count':
                return sorted(
                    cls._instances.values(),
                    key=lambda x: x.article_count(),
                    reverse=True
                )
            elif kwargs['sort_by'] == 'label':
                return sorted(
                    cls._instances.values(),
                    key=lambda x: x.names['en']
                )
        return list(cls._instances.values())
