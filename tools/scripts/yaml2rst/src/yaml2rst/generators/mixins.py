"""Mixin classes for common generator functionality."""
from typing import Dict, Any, List


class RelationshipMixin:
    """Mixin providing unified access to RelationshipManager.

    This mixin provides a lazy-loaded RelationshipManager instance
    to eliminate code duplication across generators.
    """

    @property
    def relationship_manager(self):
        """Get RelationshipManager instance (lazy-loaded).

        Returns:
            RelationshipManager: Singleton instance of RelationshipManager
        """
        if not hasattr(self, '_relationship_manager'):
            # Import here to allow for proper mocking in tests
            from freee_a11y_gl.relationship_manager import RelationshipManager
            self._relationship_manager = RelationshipManager()
        return self._relationship_manager


class ValidationMixin:
    """Mixin providing common validation functionality.

    This mixin consolidates common validation patterns used across
    different generator classes.
    """

    def validate_required_fields(self, data: Dict[str, Any],
                                 required_fields: List[str]) -> bool:
        """Validate that all required fields are present in data.

        Args:
            data: Data dictionary to validate
            required_fields: List of required field names

        Returns:
            bool: True if all required fields are present, False otherwise
        """
        return all(field in data for field in required_fields)

    def validate_list_field(self, data: Dict[str, Any],
                            field_name: str) -> bool:
        """Validate that a field exists and is a list.

        Args:
            data: Data dictionary to validate
            field_name: Name of the field to validate

        Returns:
            bool: True if field exists and is a list, False otherwise
        """
        return field_name in data and isinstance(data[field_name], list)

    def validate_string_field(self, data: Dict[str, Any], field_name: str,
                              allow_empty: bool = False) -> bool:
        """Validate that a field exists and is a non-empty string.

        Args:
            data: Data dictionary to validate
            field_name: Name of the field to validate
            allow_empty: Whether to allow empty strings

        Returns:
            bool: True if field is valid string, False otherwise
        """
        if field_name not in data:
            return False

        value = data[field_name]
        if not isinstance(value, str):
            return False

        return allow_empty or len(value.strip()) > 0


class UtilityMixin:
    """Mixin providing common utility methods for generators.

    This mixin provides helper methods for common operations like
    sorting objects and processing template data.
    """

    def get_sorted_objects(self, objects: List[Any],
                           sort_key: str = 'sort_key') -> List[Any]:
        """Sort objects by a specified attribute.

        Args:
            objects: List of objects to sort
            sort_key: Attribute name to sort by

        Returns:
            List of sorted objects
        """
        return sorted(objects, key=lambda x: getattr(x, sort_key, ''))

    def get_sorted_objects_by_lang_name(self, objects: List[Any],
                                        lang: str) -> List[Any]:
        """Sort objects by their localized name.

        Args:
            objects: List of objects to sort (must have 'names' attribute)
            lang: Language code

        Returns:
            List of objects sorted by localized name
        """
        return sorted(objects, key=lambda x: getattr(
            x, 'names', {}).get(lang, ''))

    def process_template_data(self, obj: Any, lang: str) -> Dict[str, Any]:
        """Process an object into template data.

        Args:
            obj: Object to process (must have template_data method)
            lang: Language code

        Returns:
            Template data dictionary
        """
        if hasattr(obj, 'template_data'):
            return obj.template_data(lang)
        return {}

    def process_template_data_list(self, objects: List[Any],
                                   lang: str) -> List[Dict[str, Any]]:
        """Process a list of objects into template data.

        Args:
            objects: List of objects to process
            lang: Language code

        Returns:
            List of template data dictionaries
        """
        return [self.process_template_data(obj, lang) for obj in objects]

    def filter_objects_with_articles(self, objects: List[Any]) -> List[Any]:
        """Filter objects that have associated articles.

        Args:
            objects: List of objects to filter (must have article_count
                     method)

        Returns:
            List of objects with articles
        """
        return [obj for obj in objects if hasattr(obj, 'article_count')
                and obj.article_count() > 0]
