"""Common base classes for specific types of generators."""
from typing import Dict, Any, Iterator, TypeVar, Generic, List
from abc import abstractmethod

from .content_generator_base import ContentGeneratorBase

T = TypeVar('T')


class ListBasedGenerator(ContentGeneratorBase, Generic[T]):
    """Base class for generators that process lists of items.

    This class extends ContentGeneratorBase to provide a standardized pattern
    for generators that process lists of items. It includes:
    - Unified RelationshipManager access via RelationshipMixin
    - Common validation methods via ValidationMixin
    - Utility methods for sorting and processing via UtilityMixin
    """

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate content from a list of items."""
        items = self.get_items()
        self.logger.info(f"Processing {len(items)} items")

        for item in items:
            try:
                data = self.process_item(item)
                if data and self.validate_data(data):
                    yield self.postprocess_data(data)
            except Exception as e:
                self.logger.error(f"Error processing item {item}: {e}")
                raise

    @abstractmethod
    def get_items(self) -> List[T]:
        """Get list of items to process."""
        raise NotImplementedError

    @abstractmethod
    def process_item(self, item: T) -> Dict[str, Any]:
        """Process a single item into template data."""
        raise NotImplementedError


class SingleFileGenerator(ContentGeneratorBase):
    """Base class for generators that produce a single file.

    This class extends ContentGeneratorBase to provide a standardized pattern
    for generators that produce single files. It includes:
    - Unified RelationshipManager access via RelationshipMixin
    - Common validation methods via ValidationMixin
    - Utility methods for sorting and processing via UtilityMixin
    """

    @abstractmethod
    def get_template_data(self) -> Dict[str, Any]:
        """Get data for the template."""
        raise NotImplementedError

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate content for a single file."""
        try:
            data = self.get_template_data()
            if data and self.validate_data(data):
                yield self.postprocess_data(data)
        except Exception as e:
            self.logger.error(f"Error generating template data: {e}")
            raise
