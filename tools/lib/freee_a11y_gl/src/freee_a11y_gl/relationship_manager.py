"""Relationship management for accessibility guidelines entities."""
from typing import Any, List

from .models.base import BaseModel


class RelationshipManager:
    """Manages relationships between different model objects."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RelationshipManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the relationship manager.

        Uses singleton pattern to ensure only one instance exists.
        """
        if self._initialized:
            return
        self._data = {}
        self._unresolved_faqs = {}
        self._initialized = True

    def associate_objects(self, obj1: BaseModel, obj2: BaseModel) -> None:
        """Associate two objects bidirectionally.

        Args:
            obj1: First object to associate
            obj2: Second object to associate
        """
        obj1_type = obj1.object_type
        obj2_type = obj2.object_type
        obj1_id = obj1.id
        obj2_id = obj2.id

        # Create nested dictionaries if they don't exist
        for obj_type, obj_id in [(obj1_type, obj1_id), (obj2_type, obj2_id)]:
            if obj_type not in self._data:
                self._data[obj_type] = {}
            if obj_id not in self._data[obj_type]:
                self._data[obj_type][obj_id] = {}

        # Add bidirectional relationship
        for (src_type, src_id, src_obj, dest_type, dest_obj) in [
            (obj1_type, obj1_id, obj1, obj2_type, obj2),
            (obj2_type, obj2_id, obj2, obj1_type, obj1)
        ]:
            if dest_type not in self._data[src_type][src_id]:
                self._data[src_type][src_id][dest_type] = []
            if dest_obj not in self._data[src_type][src_id][dest_type]:
                self._data[src_type][src_id][dest_type].append(dest_obj)

    def add_unresolved_faqs(self, faq1_id: str, faq2_id: str) -> None:
        """Add unresolved FAQ relationship to be resolved later.

        Args:
            faq1_id: ID of first FAQ
            faq2_id: ID of second FAQ
        """
        for id1, id2 in [(faq1_id, faq2_id), (faq2_id, faq1_id)]:
            if id1 not in self._unresolved_faqs:
                self._unresolved_faqs[id1] = []
            if id2 not in self._unresolved_faqs[id1]:
                self._unresolved_faqs[id1].append(id2)

    def resolve_faqs(self) -> None:
        """Resolve all unresolved FAQ relationships."""
        from .models.faq.article import Faq  # Import here to avoid circular imports

        for faq_id in self._unresolved_faqs:
            for faq2_id in self._unresolved_faqs[faq_id]:
                faq1 = Faq.get_by_id(faq_id)
                faq2 = Faq.get_by_id(faq2_id)
                if faq1 and faq2:
                    self.associate_objects(faq1, faq2)

    def get_related_objects(self, obj: BaseModel, related_type: str) -> List[Any]:
        """Get all related objects of a specific type for an object.

        Args:
            obj: Source object
            related_type: Type of related objects to retrieve

        Returns:
            List of related objects
        """
        try:
            return self._data[obj.object_type][obj.id][related_type]
        except KeyError:
            return []

    def get_sorted_related_objects(
        self,
        obj: BaseModel,
        related_type: str,
        key: str = 'sort_key'
    ) -> List[Any]:
        """Get sorted related objects of a specific type.

        Args:
            obj: Source object
            related_type: Type of related objects to get
            key: Key to sort by (defaults to 'sort_key')

        Returns:
            Sorted list of related objects
        """
        objects = self.get_related_objects(obj, related_type)
        return sorted(objects, key=lambda x: getattr(x, key))
