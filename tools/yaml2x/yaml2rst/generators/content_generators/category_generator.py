"""Generator for category pages."""
from typing import Dict, Any, Iterator, List

from freee_a11y_gl import Category
from freee_a11y_gl.relationship_manager import RelationshipManager
from ..common_generators import ListBasedGenerator

class CategoryGenerator(ListBasedGenerator[str]):
    """Generates category pages with associated guidelines."""

    def __init__(self, lang: str):
        super().__init__(lang)
        self.relationship_manager = RelationshipManager()
        self.categories_by_id = {cat.id: cat for cat in Category.list_all()}

    def get_items(self) -> List[str]:
        """Get all category IDs to process."""
        return list(self.categories_by_id.keys())

    def process_item(self, category_id: str) -> Dict[str, Any]:
        """Process a single category."""
        category_map = self.relationship_manager.get_guidelines_to_category()
        category = self.categories_by_id[category_id]
        guidelines = category_map[category_id]
        return {
            'filename': category_id,
            'guidelines': [gl.template_data(self.lang) for gl in guidelines]
        }

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate category page data."""
        required_fields = ['filename', 'guidelines']
        return all(field in data for field in required_fields)

    def get_dependencies(self) -> list[str]:
        """Get category file dependencies."""
        return [cat.get_dependency() for cat in Category.list_all()]
