"""Generator for category pages."""
from typing import Dict, Any, Iterator

from a11y_guidelines import RelationshipManager, Category
from ..base_generator import BaseGenerator

class CategoryGenerator(BaseGenerator):
    """Generates category pages with associated guidelines."""

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate category page data.
        
        Yields:
            Dictionary containing category and its guidelines data
        """
        rel = RelationshipManager()
        for category, guidelines in rel.get_guidelines_to_category().items():
            yield {
                'filename': category,
                'guidelines': [gl.template_data(self.lang) for gl in guidelines]
            }

    def get_dependencies(self) -> list[str]:
        """Get category file dependencies.
        
        Returns:
            List of category source file paths
        """
        return [cat.get_dependency() for cat in Category.list_all()]
