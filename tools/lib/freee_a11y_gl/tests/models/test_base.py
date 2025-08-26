from freee_a11y_gl.models.base import BaseModel


class ConcreteModel(BaseModel):
    """Concrete implementation of BaseModel for testing."""

    object_type = "test_model"
    _instances = {}

    def __init__(self, id: str, extra_data: str = None):
        """Initialize concrete model for testing.

        Args:
            id: Model identifier
            extra_data: Additional test data
        """
        super().__init__(id)
        self.extra_data = extra_data
        ConcreteModel._instances[id] = self


class TestBaseModel:
    """Test cases for BaseModel class."""

    def setup_method(self):
        """Setup for each test method."""
        # Clear all instances before each test
        ConcreteModel._instances.clear()

    def test_init(self):
        """Test BaseModel initialization."""
        model = ConcreteModel("test-id")
        assert model.id == "test-id"
        assert model.object_type == "test_model"
        assert hasattr(ConcreteModel, '_instances')

    def test_init_creates_instances_dict_if_not_exists(self):
        """Test that _instances dict is created if it doesn't exist."""
        # Create a new class without _instances
        class NewModel(BaseModel):
            object_type = "new_model"

        _ = NewModel("test-id")
        assert hasattr(NewModel, '_instances')
        assert isinstance(NewModel._instances, dict)

    def test_multiple_instances(self):
        """Test creating multiple instances."""
        model1 = ConcreteModel("id1", "data1")
        model2 = ConcreteModel("id2", "data2")

        assert model1.id == "id1"
        assert model1.extra_data == "data1"
        assert model2.id == "id2"
        assert model2.extra_data == "data2"

        assert len(ConcreteModel._instances) == 2
        assert ConcreteModel._instances["id1"] == model1
        assert ConcreteModel._instances["id2"] == model2

    def test_get_by_id_existing(self):
        """Test getting existing model by ID."""
        model = ConcreteModel("test-id")
        retrieved = ConcreteModel.get_by_id("test-id")
        assert retrieved == model
        assert retrieved.id == "test-id"

    def test_get_by_id_nonexistent(self):
        """Test getting nonexistent model by ID returns None."""
        result = ConcreteModel.get_by_id("nonexistent-id")
        assert result is None

    def test_get_by_id_empty_instances(self):
        """Test getting by ID when no instances exist."""
        # Ensure instances dict is empty
        assert len(ConcreteModel._instances) == 0
        result = ConcreteModel.get_by_id("any-id")
        assert result is None

    def test_instances_isolation_between_classes(self):
        """Test that different model classes have isolated instance stores."""
        class AnotherModel(BaseModel):
            object_type = "another_model"
            _instances = {}

            def __init__(self, id: str):
                super().__init__(id)
                AnotherModel._instances[id] = self

        model1 = ConcreteModel("shared-id")
        model2 = AnotherModel("shared-id")

        # Both models can have the same ID without conflict
        assert ConcreteModel.get_by_id("shared-id") == model1
        assert AnotherModel.get_by_id("shared-id") == model2
        assert ConcreteModel.get_by_id("shared-id") != model2
        assert AnotherModel.get_by_id("shared-id") != model1

    def test_inheritance_preserves_functionality(self):
        """Test that inheritance preserves BaseModel functionality."""
        class ExtendedModel(ConcreteModel):
            object_type = "extended_model"
            _instances = {}

            def __init__(self, id: str, extended_attr: str = None):
                super().__init__(id)
                self.extended_attr = extended_attr
                ExtendedModel._instances[id] = self

        extended = ExtendedModel("extended-id", "extended-value")
        assert extended.id == "extended-id"
        assert extended.extended_attr == "extended-value"
        assert ExtendedModel.get_by_id("extended-id") == extended

    def test_type_hints_work_correctly(self):
        """Test that type hints work correctly with get_by_id."""
        _ = ConcreteModel("typed-id")

        # This should work with proper typing
        retrieved = ConcreteModel.get_by_id("typed-id")
        assert isinstance(retrieved, ConcreteModel)
        assert retrieved is not None

        # Test that the return type is correctly typed
        # (This is more for static analysis, but we can test the runtime behavior)
        nonexistent = ConcreteModel.get_by_id("nonexistent")
        assert nonexistent is None

    def test_id_attribute_immutability(self):
        """Test that ID attribute behavior is as expected."""
        model = ConcreteModel("original-id")
        assert model.id == "original-id"

        # ID can be changed (not immutable by design),
        # but this doesn't affect instance storage
        model.id = "changed-id"
        assert model.id == "changed-id"

        # Original key is still in instances
        assert ConcreteModel.get_by_id("original-id") == model
        assert ConcreteModel.get_by_id("changed-id") is None

    def test_class_attributes_vs_instance_attributes(self):
        """Test that class and instance attributes work correctly."""
        model1 = ConcreteModel("id1")
        model2 = ConcreteModel("id2")

        # object_type is a class attribute
        assert model1.object_type == "test_model"
        assert model2.object_type == "test_model"
        assert ConcreteModel.object_type == "test_model"

        # _instances is a class attribute
        assert model1._instances is ConcreteModel._instances
        assert model2._instances is ConcreteModel._instances

        # id is an instance attribute
        assert model1.id != model2.id

    def test_empty_string_id(self):
        """Test behavior with empty string ID."""
        model = ConcreteModel("")
        assert model.id == ""
        assert ConcreteModel.get_by_id("") == model

    def test_none_id_behavior(self):
        """Test behavior when None is passed as ID."""
        # This should work since the type hint allows Any for compatibility
        model = ConcreteModel(None)
        assert model.id is None
        assert ConcreteModel.get_by_id(None) == model

    def test_numeric_id(self):
        """Test behavior with numeric ID (converted to string)."""
        # If numeric IDs are passed, they should work
        model = ConcreteModel(123)
        assert model.id == 123
        assert ConcreteModel.get_by_id(123) == model
