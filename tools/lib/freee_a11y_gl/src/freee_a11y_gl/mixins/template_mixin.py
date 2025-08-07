"""Template data generation mixin for models."""
from typing import Any, Dict, List
from ..utils import join_items


class TemplateDataMixin:
    """Mixin providing common template data generation functionality."""

    def get_base_template_data(self, lang: str) -> Dict[str, Any]:
        """Generate basic template data common to all models.

        Args:
            lang: Language code ('ja' or 'en')

        Returns:
            Dictionary with basic template data
        """
        data = {
            'id': self.id,
        }

        # Add title if available
        if hasattr(self, 'title') and self.title:
            data['title'] = self.title.get(lang, '')

        return data

    def add_related_objects(self, data: Dict[str, Any],
                            object_type: str) -> None:
        """Add related objects to template data.

        Args:
            data: Template data dictionary to modify
            object_type: Type of related objects to add ('faq', 'info_ref')
        """
        rel = self._get_relationship_manager()
        related_objects = rel.get_sorted_related_objects(self, object_type)

        if related_objects:
            # Use plural form for the key
            plural_key = f'{object_type}s'
            if object_type == 'info_ref':
                data[plural_key] = [obj.refstring()
                                    for obj in related_objects]
            else:
                data[plural_key] = [obj.id for obj in related_objects]

    def add_link_data(self, data: Dict[str, Any], lang: str,
                      base_url: str, path_template: str) -> None:
        """Add link data with text and URL for given language.

        Args:
            data: Template data dictionary to modify
            lang: Language code
            base_url: Base URL for the link
            path_template: Template path (with {id} placeholder)
        """
        if not data.get('text'):
            data['text'] = {}
        if not data.get('url'):
            data['url'] = {}

        if hasattr(self, 'title') and self.title:
            data['text'][lang] = self.title.get(lang, '')
            template_url = path_template.format(id=self.id)
            data['url'][lang] = f"{base_url}{template_url}"

    def join_platform_items(self, items: List[str], lang: str) -> str:
        """Join platform items with localized separator and platform names.

        Args:
            items: List of platform identifiers
            lang: Language code ('ja' or 'en')

        Returns:
            Joined string with localized platform names
        """
        return join_items(items, lang)

    @staticmethod
    def join_items(items: List[str], lang: str) -> str:
        """Join platform items with localized separator and platform names.

        Static method for backward compatibility with existing tests.

        Args:
            items: List of platform identifiers
            lang: Language code ('ja' or 'en')

        Returns:
            Joined string with localized platform names
        """
        return join_items(items, lang)
