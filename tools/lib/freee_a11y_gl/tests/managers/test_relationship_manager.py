import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.relationship_manager import RelationshipManager
from freee_a11y_gl.models.base import BaseModel


class MockModel(BaseModel):
    """Mock model for testing relationships."""
    
    def __init__(self, id: str, object_type: str, sort_key: str = None):
        super().__init__(id)
        self.object_type = object_type
        self.sort_key = sort_key or id


class TestRelationshipManager:
    """Test cases for RelationshipManager class."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset singleton instance for each test
        RelationshipManager._instance = None
        RelationshipManager._initialized = False

    def test_singleton_pattern(self):
        """Test that RelationshipManager follows singleton pattern."""
        manager1 = RelationshipManager()
        manager2 = RelationshipManager()
        
        assert manager1 is manager2
        assert id(manager1) == id(manager2)

    def test_init_only_once(self):
        """Test that initialization only happens once."""
        manager1 = RelationshipManager()
        initial_data = manager1._data
        
        manager2 = RelationshipManager()
        assert manager2._data is initial_data

    def test_associate_objects_basic(self):
        """Test basic object association."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        
        manager.associate_objects(obj1, obj2)
        
        # Check bidirectional relationship
        assert obj2 in manager.get_related_objects(obj1, "type2")
        assert obj1 in manager.get_related_objects(obj2, "type1")

    def test_associate_objects_same_type(self):
        """Test associating objects of the same type."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "same_type")
        obj2 = MockModel("obj2", "same_type")
        
        manager.associate_objects(obj1, obj2)
        
        # Check bidirectional relationship within same type
        assert obj2 in manager.get_related_objects(obj1, "same_type")
        assert obj1 in manager.get_related_objects(obj2, "same_type")

    def test_associate_multiple_objects(self):
        """Test associating multiple objects."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        obj3 = MockModel("obj3", "type2")
        
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj3)
        
        # obj1 should be related to both obj2 and obj3
        related_type2 = manager.get_related_objects(obj1, "type2")
        assert len(related_type2) == 2
        assert obj2 in related_type2
        assert obj3 in related_type2
        
        # obj2 and obj3 should both be related to obj1
        assert obj1 in manager.get_related_objects(obj2, "type1")
        assert obj1 in manager.get_related_objects(obj3, "type1")

    def test_associate_objects_no_duplicates(self):
        """Test that associating the same objects multiple times doesn't create duplicates."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        
        # Associate the same objects multiple times
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj2)
        
        # Should only have one relationship each way
        assert len(manager.get_related_objects(obj1, "type2")) == 1
        assert len(manager.get_related_objects(obj2, "type1")) == 1

    def test_get_related_objects_empty(self):
        """Test getting related objects when none exist."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        
        # Should return empty list for non-existent relationships
        result = manager.get_related_objects(obj1, "nonexistent_type")
        assert result == []

    def test_get_related_objects_nonexistent_object(self):
        """Test getting related objects for non-existent object."""
        manager = RelationshipManager()
        
        obj1 = MockModel("nonexistent", "type1")
        
        # Should return empty list for non-existent object
        result = manager.get_related_objects(obj1, "type2")
        assert result == []

    def test_add_unresolved_faqs(self):
        """Test adding unresolved FAQ relationships."""
        manager = RelationshipManager()
        
        manager.add_unresolved_faqs("faq1", "faq2")
        
        # Check bidirectional unresolved relationships
        assert "faq2" in manager._unresolved_faqs["faq1"]
        assert "faq1" in manager._unresolved_faqs["faq2"]

    def test_add_unresolved_faqs_multiple(self):
        """Test adding multiple unresolved FAQ relationships."""
        manager = RelationshipManager()
        
        manager.add_unresolved_faqs("faq1", "faq2")
        manager.add_unresolved_faqs("faq1", "faq3")
        manager.add_unresolved_faqs("faq2", "faq3")
        
        # faq1 should be related to faq2 and faq3
        assert set(manager._unresolved_faqs["faq1"]) == {"faq2", "faq3"}
        # faq2 should be related to faq1 and faq3
        assert set(manager._unresolved_faqs["faq2"]) == {"faq1", "faq3"}
        # faq3 should be related to faq1 and faq2
        assert set(manager._unresolved_faqs["faq3"]) == {"faq1", "faq2"}

    def test_add_unresolved_faqs_no_duplicates(self):
        """Test that adding same FAQ relationships doesn't create duplicates."""
        manager = RelationshipManager()
        
        manager.add_unresolved_faqs("faq1", "faq2")
        manager.add_unresolved_faqs("faq1", "faq2")  # Duplicate
        manager.add_unresolved_faqs("faq2", "faq1")  # Reverse order
        
        # Should only have one relationship each way
        assert manager._unresolved_faqs["faq1"] == ["faq2"]
        assert manager._unresolved_faqs["faq2"] == ["faq1"]

    @patch('freee_a11y_gl.models.faq.article.Faq')
    def test_resolve_faqs_success(self, mock_faq_class):
        """Test successful FAQ resolution."""
        manager = RelationshipManager()
        
        # Setup mocks
        mock_faq1 = MockModel("faq1", "faq")
        mock_faq2 = MockModel("faq2", "faq")
        
        mock_faq_class.get_by_id.side_effect = lambda faq_id: {
            "faq1": mock_faq1,
            "faq2": mock_faq2
        }.get(faq_id)
        
        # Add unresolved relationships
        manager.add_unresolved_faqs("faq1", "faq2")
        
        # Resolve FAQs
        manager.resolve_faqs()
        
        # Check that relationships were created
        assert mock_faq2 in manager.get_related_objects(mock_faq1, "faq")
        assert mock_faq1 in manager.get_related_objects(mock_faq2, "faq")

    @patch('freee_a11y_gl.models.faq.article.Faq')
    def test_resolve_faqs_missing_objects(self, mock_faq_class):
        """Test FAQ resolution when some objects are missing."""
        manager = RelationshipManager()
        
        # Setup mocks - only faq1 exists
        mock_faq1 = MockModel("faq1", "faq")
        
        mock_faq_class.get_by_id.side_effect = lambda faq_id: {
            "faq1": mock_faq1,
            "faq2": None  # faq2 doesn't exist
        }.get(faq_id)
        
        # Add unresolved relationships
        manager.add_unresolved_faqs("faq1", "faq2")
        
        # Resolve FAQs - should not crash
        manager.resolve_faqs()
        
        # No relationships should be created since faq2 doesn't exist
        assert manager.get_related_objects(mock_faq1, "faq") == []

    def test_get_sorted_related_objects(self):
        """Test getting sorted related objects."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2", "z_sort")
        obj3 = MockModel("obj3", "type2", "a_sort")
        obj4 = MockModel("obj4", "type2", "m_sort")
        
        # Associate objects in random order
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj4)
        manager.associate_objects(obj1, obj3)
        
        # Get sorted related objects
        sorted_objects = manager.get_sorted_related_objects(obj1, "type2")
        
        # Should be sorted by sort_key
        assert len(sorted_objects) == 3
        assert sorted_objects[0] == obj3  # a_sort
        assert sorted_objects[1] == obj4  # m_sort
        assert sorted_objects[2] == obj2  # z_sort

    def test_get_sorted_related_objects_custom_key(self):
        """Test getting sorted related objects with custom sort key."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        obj2.custom_sort = "z"
        obj3 = MockModel("obj3", "type2")
        obj3.custom_sort = "a"
        
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj3)
        
        # Get sorted by custom key
        sorted_objects = manager.get_sorted_related_objects(obj1, "type2", "custom_sort")
        
        assert sorted_objects[0] == obj3  # custom_sort = "a"
        assert sorted_objects[1] == obj2  # custom_sort = "z"

    def test_get_sorted_related_objects_empty(self):
        """Test getting sorted related objects when none exist."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        
        # Should return empty list
        result = manager.get_sorted_related_objects(obj1, "nonexistent_type")
        assert result == []

    def test_data_structure_integrity(self):
        """Test that internal data structure maintains integrity."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        obj3 = MockModel("obj3", "type1")
        
        manager.associate_objects(obj1, obj2)
        manager.associate_objects(obj1, obj3)
        
        # Check data structure
        assert "type1" in manager._data
        assert "type2" in manager._data
        assert "obj1" in manager._data["type1"]
        assert "obj2" in manager._data["type2"]
        assert "obj3" in manager._data["type1"]
        
        # Check relationship directions
        assert obj2 in manager._data["type1"]["obj1"]["type2"]
        assert obj3 in manager._data["type1"]["obj1"]["type1"]
        assert obj1 in manager._data["type2"]["obj2"]["type1"]
        assert obj1 in manager._data["type1"]["obj3"]["type1"]

    def test_complex_relationship_network(self):
        """Test complex network of relationships."""
        manager = RelationshipManager()
        
        # Create a network: guideline -> checks -> faqs
        guideline = MockModel("gl1", "guideline")
        check1 = MockModel("check1", "check")
        check2 = MockModel("check2", "check")
        faq1 = MockModel("faq1", "faq")
        faq2 = MockModel("faq2", "faq")
        
        # Build relationships
        manager.associate_objects(guideline, check1)
        manager.associate_objects(guideline, check2)
        manager.associate_objects(check1, faq1)
        manager.associate_objects(check2, faq1)
        manager.associate_objects(check2, faq2)
        
        # Test traversal
        related_checks = manager.get_related_objects(guideline, "check")
        assert len(related_checks) == 2
        assert check1 in related_checks
        assert check2 in related_checks
        
        related_faqs_from_check1 = manager.get_related_objects(check1, "faq")
        assert len(related_faqs_from_check1) == 1
        assert faq1 in related_faqs_from_check1
        
        related_faqs_from_check2 = manager.get_related_objects(check2, "faq")
        assert len(related_faqs_from_check2) == 2
        assert faq1 in related_faqs_from_check2
        assert faq2 in related_faqs_from_check2

    def test_memory_efficiency(self):
        """Test that the same object references are maintained."""
        manager = RelationshipManager()
        
        obj1 = MockModel("obj1", "type1")
        obj2 = MockModel("obj2", "type2")
        
        manager.associate_objects(obj1, obj2)
        
        # Retrieved objects should be the same instances
        retrieved_obj2 = manager.get_related_objects(obj1, "type2")[0]
        retrieved_obj1 = manager.get_related_objects(obj2, "type1")[0]
        
        assert retrieved_obj2 is obj2
        assert retrieved_obj1 is obj1
