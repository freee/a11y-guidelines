"""Enhanced base class for content generators with mixin functionality."""
from typing import Dict, Any, List
from .base_generator import BaseGenerator
from .mixins import RelationshipMixin, ValidationMixin, UtilityMixin


class ContentGeneratorBase(BaseGenerator, RelationshipMixin,
                           ValidationMixin, UtilityMixin):
    """Enhanced base class for content generators.

    This class combines BaseGenerator with common mixins to provide
    a comprehensive base for content generation with:
    - Unified RelationshipManager access
    - Common validation methods
    - Utility methods for sorting and processing
    """

    def __init__(self, lang: str, base_dir=None):
        """Initialize the content generator.

        Args:
            lang: Language code for content generation
            base_dir: Base directory for file operations (optional)
        """
        super().__init__(lang, base_dir)

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Default validation implementation.

        Subclasses should override this method to provide specific
        validation.

        Args:
            data: Data to validate

        Returns:
            bool: True if data is valid
        """
        return True

    def get_sorted_related_objects(self, obj, related_type: str,
                                   key: str = 'sort_key') -> List[Any]:
        """Get sorted related objects using RelationshipManager.

        This is a convenience method that combines relationship lookup
        with sorting.

        Args:
            obj: Source object
            related_type: Type of related objects to retrieve
            key: Attribute to sort by

        Returns:
            List of sorted related objects
        """
        return self.relationship_manager.get_sorted_related_objects(
            obj, related_type, key)

    def get_related_objects(self, obj, related_type: str) -> List[Any]:
        """Get related objects using RelationshipManager.

        Args:
            obj: Source object
            related_type: Type of related objects to retrieve

        Returns:
            List of related objects
        """
        return self.relationship_manager.get_related_objects(
            obj, related_type)
