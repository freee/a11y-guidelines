"""Unit tests for ContentGeneratorBase."""
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from yaml2rst.generators.content_generator_base import ContentGeneratorBase


class TestContentGeneratorBase:
    """Test ContentGeneratorBase functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        class ConcreteGenerator(ContentGeneratorBase):
            def generate(self):
                yield {'test': 'data'}
        
        self.ConcreteGenerator = ConcreteGenerator
    
    def test_initialization(self):
        """Test ContentGeneratorBase initialization."""
        generator = self.ConcreteGenerator('en')
        
        assert generator.lang == 'en'
        assert generator.context.lang == 'en'
        assert isinstance(generator.context.base_dir, Path)
    
    def test_initialization_with_base_dir(self):
        """Test ContentGeneratorBase initialization with base directory."""
        base_dir = Path('/test/path')
        generator = self.ConcreteGenerator('ja', base_dir)
        
        assert generator.lang == 'ja'
        assert generator.context.base_dir == base_dir
    
    def test_default_validate_data(self):
        """Test default validate_data implementation."""
        generator = self.ConcreteGenerator('en')
        
        # Default implementation should return True
        assert generator.validate_data({}) is True
        assert generator.validate_data({'key': 'value'}) is True
    
    def test_has_relationship_mixin(self):
        """Test that ContentGeneratorBase has RelationshipMixin functionality."""
        generator = self.ConcreteGenerator('en')
        
        # Should have relationship_manager property
        assert hasattr(generator, 'relationship_manager')
        
        # Test that relationship_manager returns an instance
        result = generator.relationship_manager
        assert result is not None
        assert hasattr(result, '__class__')
        
        # Test lazy loading - second access should return same instance
        result2 = generator.relationship_manager
        assert result is result2
    
    def test_has_validation_mixin(self):
        """Test that ContentGeneratorBase has ValidationMixin functionality."""
        generator = self.ConcreteGenerator('en')
        
        # Should have validation methods
        assert hasattr(generator, 'validate_required_fields')
        assert hasattr(generator, 'validate_list_field')
        assert hasattr(generator, 'validate_string_field')
        
        # Test validation methods work
        data = {'field1': 'value1', 'list_field': [1, 2, 3]}
        assert generator.validate_required_fields(data, ['field1']) is True
        assert generator.validate_list_field(data, 'list_field') is True
        assert generator.validate_string_field(data, 'field1') is True
    
    def test_has_utility_mixin(self):
        """Test that ContentGeneratorBase has UtilityMixin functionality."""
        generator = self.ConcreteGenerator('en')
        
        # Should have utility methods
        assert hasattr(generator, 'get_sorted_objects')
        assert hasattr(generator, 'get_sorted_objects_by_lang_name')
        assert hasattr(generator, 'process_template_data')
        assert hasattr(generator, 'process_template_data_list')
        assert hasattr(generator, 'filter_objects_with_articles')
        
        # Test utility methods work
        class MockObject:
            def __init__(self, sort_key):
                self.sort_key = sort_key
        
        objects = [MockObject('c'), MockObject('a'), MockObject('b')]
        sorted_objects = generator.get_sorted_objects(objects)
        assert len(sorted_objects) == 3
        assert sorted_objects[0].sort_key == 'a'
    
    def test_get_sorted_related_objects(self):
        """Test get_sorted_related_objects convenience method."""
        generator = self.ConcreteGenerator('en')
        
        # Mock the relationship manager
        with patch('freee_a11y_gl.relationship_manager.RelationshipManager') as mock_rm:
            mock_instance = Mock()
            mock_rm.return_value = mock_instance
            
            # Mock return value
            mock_objects = [Mock(), Mock()]
            mock_instance.get_sorted_related_objects.return_value = mock_objects
            
            # Test the convenience method
            mock_obj = Mock()
            result = generator.get_sorted_related_objects(mock_obj, 'test_type', 'test_key')
            
            assert result is mock_objects
            mock_instance.get_sorted_related_objects.assert_called_once_with(
                mock_obj, 'test_type', 'test_key'
            )
    
    def test_get_related_objects(self):
        """Test get_related_objects convenience method."""
        generator = self.ConcreteGenerator('en')
        
        # Mock the relationship manager
        with patch('freee_a11y_gl.relationship_manager.RelationshipManager') as mock_rm:
            mock_instance = Mock()
            mock_rm.return_value = mock_instance
            
            # Mock return value
            mock_objects = [Mock(), Mock()]
            mock_instance.get_related_objects.return_value = mock_objects
            
            # Test the convenience method
            mock_obj = Mock()
            result = generator.get_related_objects(mock_obj, 'test_type')
            
            assert result is mock_objects
            mock_instance.get_related_objects.assert_called_once_with(
                mock_obj, 'test_type'
            )
    
    def test_inherits_from_base_generator(self):
        """Test that ContentGeneratorBase inherits from BaseGenerator."""
        generator = self.ConcreteGenerator('en')
        
        # Should have BaseGenerator methods
        assert hasattr(generator, 'generate')
        assert hasattr(generator, 'get_dependencies')
        assert hasattr(generator, 'preprocess_data')
        assert hasattr(generator, 'postprocess_data')
        assert hasattr(generator, 'process_single_item')
        assert hasattr(generator, 'cleanup')
        
        # Should have logger
        assert hasattr(generator, 'logger')
        assert generator.logger.name == 'ConcreteGenerator'
    
    def test_context_manager_support(self):
        """Test that ContentGeneratorBase supports context manager protocol."""
        generator = self.ConcreteGenerator('en')
        
        # Should support context manager
        with generator as g:
            assert g is generator
        
        # cleanup should be called on exit (though it's a no-op in base class)
        # This test just ensures the context manager protocol works
    
    def test_multiple_inheritance_resolution(self):
        """Test that multiple inheritance is resolved correctly."""
        generator = self.ConcreteGenerator('en')
        
        # Test that we can access methods from all parent classes
        # BaseGenerator method
        assert generator.get_dependencies() == []
        
        # ValidationMixin method
        assert generator.validate_required_fields({'a': 1}, ['a']) is True
        
        # UtilityMixin method
        assert generator.get_sorted_objects([]) == []
        
        # RelationshipMixin property (lazy-loaded)
        with patch('freee_a11y_gl.relationship_manager.RelationshipManager'):
            assert hasattr(generator.relationship_manager, '__class__')


class TestContentGeneratorBaseSubclass:
    """Test ContentGeneratorBase subclassing."""
    
    def test_subclass_can_override_validate_data(self):
        """Test that subclasses can override validate_data."""
        class TestGenerator(ContentGeneratorBase):
            def validate_data(self, data):
                return 'test_field' in data
            
            def generate(self):
                yield {'test': 'data'}
        
        generator = TestGenerator('en')
        
        assert generator.validate_data({'test_field': 'value'}) is True
        assert generator.validate_data({'other_field': 'value'}) is False
    
    def test_subclass_can_implement_generate(self):
        """Test that subclasses can implement generate method."""
        class TestGenerator(ContentGeneratorBase):
            def generate(self):
                yield {'test': 'data'}
        
        generator = TestGenerator('en')
        
        result = list(generator.generate())
        assert len(result) == 1
        assert result[0] == {'test': 'data'}
    
    def test_subclass_inherits_all_functionality(self):
        """Test that subclasses inherit all mixin functionality."""
        class TestGenerator(ContentGeneratorBase):
            def generate(self):
                # Use validation mixin
                data = {'items': [1, 2, 3]}
                if self.validate_list_field(data, 'items'):
                    yield data
        
        generator = TestGenerator('en')
        
        result = list(generator.generate())
        assert len(result) == 1
        assert result[0] == {'items': [1, 2, 3]}
