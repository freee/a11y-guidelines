"""Tests for common generators module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from yaml2rst.generators.common_generators import ListBasedGenerator, SingleFileGenerator
from yaml2rst.generators.content_generator_base import ContentGeneratorBase


class MockListBasedGenerator(ListBasedGenerator[str]):
    """Mock implementation of ListBasedGenerator for testing."""
    
    def __init__(self, lang: str, items: List[str] = None, should_fail: bool = False):
        super().__init__(lang)
        self._items = items or []
        self._should_fail = should_fail
        self._process_call_count = 0
    
    def get_items(self) -> List[str]:
        """Get list of items to process."""
        return self._items
    
    def process_item(self, item: str) -> Dict[str, Any]:
        """Process a single item into template data."""
        self._process_call_count += 1
        if self._should_fail and item == 'fail_item':
            raise ValueError(f"Failed to process item: {item}")
        return {
            'filename': f'{item}.rst',
            'content': f'Content for {item}',
            'processed': True
        }
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate processed data."""
        return 'filename' in data and 'content' in data


class MockSingleFileGenerator(SingleFileGenerator):
    """Mock implementation of SingleFileGenerator for testing."""
    
    def __init__(self, lang: str, template_data: Dict[str, Any] = None, should_fail: bool = False):
        super().__init__(lang)
        self._template_data = template_data or {'content': 'test content'}
        self._should_fail = should_fail
    
    def get_template_data(self) -> Dict[str, Any]:
        """Get data for the template."""
        if self._should_fail:
            raise RuntimeError("Failed to get template data")
        return self._template_data
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate template data."""
        return 'content' in data


class TestListBasedGenerator:
    """Test ListBasedGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = MockListBasedGenerator('ja')
        assert generator.lang == 'ja'

    def test_get_items_not_implemented(self):
        """Test that get_items raises NotImplementedError when not implemented."""
        # Create a subclass that implements process_item but calls super() for get_items
        class IncompleteListGenerator(ListBasedGenerator[str]):
            def get_items(self) -> List[str]:
                return super().get_items()
            
            def process_item(self, item: str) -> Dict[str, Any]:
                return {'test': 'data'}
        
        generator = IncompleteListGenerator('ja')
        
        with pytest.raises(NotImplementedError):
            generator.get_items()

    def test_process_item_not_implemented(self):
        """Test that process_item raises NotImplementedError when not implemented."""
        # Create a subclass that implements get_items but calls super() for process_item
        class IncompleteListGenerator(ListBasedGenerator[str]):
            def get_items(self) -> List[str]:
                return ['test']
            
            def process_item(self, item: str) -> Dict[str, Any]:
                return super().process_item(item)
        
        generator = IncompleteListGenerator('ja')
        
        with pytest.raises(NotImplementedError):
            generator.process_item('test')
    
    def test_generate_success(self):
        """Test successful generation with multiple items."""
        items = ['item1', 'item2', 'item3']
        generator = MockListBasedGenerator('ja', items)
        generator.logger = Mock()
        
        results = list(generator.generate())
        
        assert len(results) == 3
        assert results[0]['filename'] == 'item1.rst'
        assert results[1]['filename'] == 'item2.rst'
        assert results[2]['filename'] == 'item3.rst'
        
        # Verify logging
        generator.logger.info.assert_called_once_with("Processing 3 items")
        
        # Verify all items were processed
        assert generator._process_call_count == 3
    
    def test_generate_empty_items(self):
        """Test generation with no items."""
        generator = MockListBasedGenerator('ja', [])
        generator.logger = Mock()
        
        results = list(generator.generate())
        
        assert len(results) == 0
        generator.logger.info.assert_called_once_with("Processing 0 items")
        assert generator._process_call_count == 0
    
    def test_generate_with_postprocessing(self):
        """Test generation with postprocessing."""
        items = ['item1']
        generator = MockListBasedGenerator('ja', items)
        generator.logger = Mock()
        
        # Mock postprocess_data to add extra field
        original_postprocess = generator.postprocess_data
        def mock_postprocess(data):
            data = original_postprocess(data)
            data['postprocessed'] = True
            return data
        generator.postprocess_data = mock_postprocess
        
        results = list(generator.generate())
        
        assert len(results) == 1
        assert results[0]['filename'] == 'item1.rst'
        assert results[0]['postprocessed'] is True
    
    def test_generate_validation_failure(self):
        """Test generation with validation failure."""
        items = ['item1']
        generator = MockListBasedGenerator('ja', items)
        generator.logger = Mock()
        
        # Mock validate_data to always return False
        generator.validate_data = Mock(return_value=False)
        
        results = list(generator.generate())
        
        # Should skip invalid items
        assert len(results) == 0
        assert generator._process_call_count == 1  # Item was processed
        generator.validate_data.assert_called_once()
    
    def test_generate_processing_exception(self):
        """Test generation with processing exception."""
        items = ['good_item', 'fail_item', 'another_good_item']
        generator = MockListBasedGenerator('ja', items, should_fail=True)
        generator.logger = Mock()
        
        # Should raise exception when processing fails
        with pytest.raises(ValueError, match="Failed to process item: fail_item"):
            list(generator.generate())
        
        # Should have logged error
        generator.logger.error.assert_called_once()
        assert "Error processing item fail_item" in str(generator.logger.error.call_args)
    
    def test_generate_empty_data_from_process_item(self):
        """Test generation when process_item returns empty data."""
        items = ['item1']
        generator = MockListBasedGenerator('ja', items)
        generator.logger = Mock()
        
        # Mock process_item to return None/empty data
        generator.process_item = Mock(return_value=None)
        
        results = list(generator.generate())
        
        # Should skip items that return no data
        assert len(results) == 0
        generator.process_item.assert_called_once_with('item1')
    
    def test_generate_invalid_data_from_process_item(self):
        """Test generation when process_item returns invalid data."""
        items = ['item1']
        generator = MockListBasedGenerator('ja', items)
        generator.logger = Mock()
        
        # Mock process_item to return data that fails validation
        generator.process_item = Mock(return_value={'invalid': 'data'})
        
        results = list(generator.generate())
        
        # Should skip items with invalid data
        assert len(results) == 0
        generator.process_item.assert_called_once_with('item1')


class TestSingleFileGenerator:
    """Test SingleFileGenerator class."""
    
    def test_init(self):
        """Test generator initialization."""
        generator = MockSingleFileGenerator('ja')
        assert generator.lang == 'ja'

    def test_get_template_data_not_implemented(self):
        """Test that get_template_data raises NotImplementedError when not implemented."""
        # Create a subclass that calls super() for get_template_data
        class IncompleteSingleGenerator(SingleFileGenerator):
            def get_template_data(self) -> Dict[str, Any]:
                return super().get_template_data()
        
        generator = IncompleteSingleGenerator('ja')
        
        with pytest.raises(NotImplementedError):
            generator.get_template_data()
    
    def test_generate_success(self):
        """Test successful generation."""
        template_data = {'content': 'test content', 'title': 'Test Title'}
        generator = MockSingleFileGenerator('ja', template_data)
        generator.logger = Mock()
        
        results = list(generator.generate())
        
        assert len(results) == 1
        assert results[0]['content'] == 'test content'
        assert results[0]['title'] == 'Test Title'
    
    def test_generate_with_postprocessing(self):
        """Test generation with postprocessing."""
        template_data = {'content': 'test content'}
        generator = MockSingleFileGenerator('ja', template_data)
        generator.logger = Mock()
        
        # Mock postprocess_data to add extra field
        original_postprocess = generator.postprocess_data
        def mock_postprocess(data):
            data = original_postprocess(data)
            data['postprocessed'] = True
            return data
        generator.postprocess_data = mock_postprocess
        
        results = list(generator.generate())
        
        assert len(results) == 1
        assert results[0]['content'] == 'test content'
        assert results[0]['postprocessed'] is True
    
    def test_generate_validation_failure(self):
        """Test generation with validation failure."""
        template_data = {'invalid': 'data'}  # Missing 'content' field
        generator = MockSingleFileGenerator('ja', template_data)
        generator.logger = Mock()
        
        results = list(generator.generate())
        
        # Should skip invalid data
        assert len(results) == 0
    
    def test_generate_template_data_exception(self):
        """Test generation with template data exception."""
        generator = MockSingleFileGenerator('ja', should_fail=True)
        generator.logger = Mock()
        
        # Should raise exception when get_template_data fails
        with pytest.raises(RuntimeError, match="Failed to get template data"):
            list(generator.generate())
        
        # Should have logged error
        generator.logger.error.assert_called_once()
        assert "Error generating template data" in str(generator.logger.error.call_args)
    
    def test_generate_empty_template_data(self):
        """Test generation when get_template_data returns empty data."""
        generator = MockSingleFileGenerator('ja')
        generator.logger = Mock()
        
        # Mock get_template_data to return None/empty data
        generator.get_template_data = Mock(return_value=None)
        
        results = list(generator.generate())
        
        # Should skip empty data
        assert len(results) == 0
        generator.get_template_data.assert_called_once()
    
    def test_generate_invalid_template_data(self):
        """Test generation when get_template_data returns invalid data."""
        generator = MockSingleFileGenerator('ja')
        generator.logger = Mock()
        
        # Mock get_template_data to return data that fails validation
        generator.get_template_data = Mock(return_value={'invalid': 'data'})
        
        results = list(generator.generate())
        
        # Should skip invalid data
        assert len(results) == 0
        generator.get_template_data.assert_called_once()


class TestGeneratorIntegration:
    """Test integration scenarios between generators."""
    
    def test_list_based_generator_inheritance(self):
        """Test that ListBasedGenerator properly inherits from BaseGenerator."""
        generator = MockListBasedGenerator('ja')
        
        # Should have BaseGenerator methods
        assert hasattr(generator, 'lang')
        assert hasattr(generator, 'get_dependencies')
        assert hasattr(generator, 'validate_data')
        assert hasattr(generator, 'preprocess_data')
        assert hasattr(generator, 'postprocess_data')
        
        # Should have its own abstract methods implemented
        assert hasattr(generator, 'get_items')
        assert hasattr(generator, 'process_item')
        assert hasattr(generator, 'generate')
    
    def test_single_file_generator_inheritance(self):
        """Test that SingleFileGenerator properly inherits from BaseGenerator."""
        generator = MockSingleFileGenerator('ja')
        
        # Should have BaseGenerator methods
        assert hasattr(generator, 'lang')
        assert hasattr(generator, 'get_dependencies')
        assert hasattr(generator, 'validate_data')
        assert hasattr(generator, 'preprocess_data')
        assert hasattr(generator, 'postprocess_data')
        
        # Should have its own abstract methods implemented
        assert hasattr(generator, 'get_template_data')
        assert hasattr(generator, 'generate')
    
    def test_generator_context_usage(self):
        """Test that generators properly use context."""
        generator = MockListBasedGenerator('ja')
        
        # Should have context with correct language
        assert generator.context.lang == 'ja'
        assert generator.lang == 'ja'  # Backward compatibility property
    
    def test_error_handling_consistency(self):
        """Test that both generator types handle errors consistently."""
        # Test ListBasedGenerator error handling
        list_gen = MockListBasedGenerator('ja', ['fail_item'], should_fail=True)
        list_gen.logger = Mock()
        
        with pytest.raises(ValueError):
            list(list_gen.generate())
        
        # Test SingleFileGenerator error handling
        single_gen = MockSingleFileGenerator('ja', should_fail=True)
        single_gen.logger = Mock()
        
        with pytest.raises(RuntimeError):
            list(single_gen.generate())
        
        # Both should have logged errors
        list_gen.logger.error.assert_called_once()
        single_gen.logger.error.assert_called_once()


class TestContentGeneratorBaseIntegration:
    """Test integration with ContentGeneratorBase and mixins."""
    
    def test_list_based_generator_inherits_content_generator_base(self):
        """Test that ListBasedGenerator inherits from ContentGeneratorBase."""
        generator = MockListBasedGenerator('ja')
        
        # Should be instance of ContentGeneratorBase
        assert isinstance(generator, ContentGeneratorBase)
        
        # Should have mixin functionality
        assert hasattr(generator, 'relationship_manager')  # RelationshipMixin
        assert hasattr(generator, 'validate_required_fields')  # ValidationMixin
        assert hasattr(generator, 'get_sorted_objects')  # UtilityMixin
    
    def test_single_file_generator_inherits_content_generator_base(self):
        """Test that SingleFileGenerator inherits from ContentGeneratorBase."""
        generator = MockSingleFileGenerator('ja')
        
        # Should be instance of ContentGeneratorBase
        assert isinstance(generator, ContentGeneratorBase)
        
        # Should have mixin functionality
        assert hasattr(generator, 'relationship_manager')  # RelationshipMixin
        assert hasattr(generator, 'validate_required_fields')  # ValidationMixin
        assert hasattr(generator, 'get_sorted_objects')  # UtilityMixin
    
    @patch('freee_a11y_gl.relationship_manager.RelationshipManager')
    def test_relationship_manager_access(self, mock_rm_class):
        """Test that generators can access RelationshipManager through mixin."""
        mock_rm_instance = Mock()
        mock_rm_class.return_value = mock_rm_instance
        
        generator = MockListBasedGenerator('ja')
        
        # Access relationship_manager should create instance
        rm = generator.relationship_manager
        
        # Should have called RelationshipManager constructor
        mock_rm_class.assert_called_once()
        assert rm == mock_rm_instance
        
        # Second access should return same instance (lazy loading)
        rm2 = generator.relationship_manager
        assert rm2 == rm
        mock_rm_class.assert_called_once()  # Should not be called again
    
    def test_validation_mixin_functionality(self):
        """Test ValidationMixin methods are available."""
        generator = MockListBasedGenerator('ja')
        
        # Test validate_required_fields
        data = {'filename': 'test.rst', 'content': 'test content'}
        assert generator.validate_required_fields(data, ['filename', 'content']) is True
        assert generator.validate_required_fields(data, ['filename', 'missing']) is False
        
        # Test validate_list_field
        data_with_list = {'items': ['item1', 'item2']}
        assert generator.validate_list_field(data_with_list, 'items') is True
        assert generator.validate_list_field(data, 'items') is False
        
        # Test validate_string_field
        assert generator.validate_string_field(data, 'filename') is True
        assert generator.validate_string_field(data, 'filename', allow_empty=False) is True
        
        empty_data = {'filename': ''}
        assert generator.validate_string_field(empty_data, 'filename', allow_empty=True) is True
        assert generator.validate_string_field(empty_data, 'filename', allow_empty=False) is False
    
    def test_utility_mixin_functionality(self):
        """Test UtilityMixin methods are available."""
        generator = MockListBasedGenerator('ja')
        
        # Create mock objects with sort_key attribute
        class MockObj:
            def __init__(self, sort_key):
                self.sort_key = sort_key
        
        objects = [MockObj('c'), MockObj('a'), MockObj('b')]
        
        # Test get_sorted_objects
        sorted_objects = generator.get_sorted_objects(objects)
        assert [obj.sort_key for obj in sorted_objects] == ['a', 'b', 'c']
        
        # Test get_sorted_objects_by_lang_name
        class MockObjWithNames:
            def __init__(self, names):
                self.names = names
        
        objects_with_names = [
            MockObjWithNames({'ja': 'ウ', 'en': 'C'}),
            MockObjWithNames({'ja': 'ア', 'en': 'A'}),
            MockObjWithNames({'ja': 'イ', 'en': 'B'})
        ]
        
        sorted_by_ja = generator.get_sorted_objects_by_lang_name(objects_with_names, 'ja')
        assert [obj.names['ja'] for obj in sorted_by_ja] == ['ア', 'イ', 'ウ']
        
        # Test process_template_data
        class MockObjWithTemplateData:
            def template_data(self, lang):
                return {'lang': lang, 'data': 'test'}
        
        obj_with_template = MockObjWithTemplateData()
        template_data = generator.process_template_data(obj_with_template, 'ja')
        assert template_data == {'lang': 'ja', 'data': 'test'}
        
        # Test process_template_data_list
        objects_with_template = [MockObjWithTemplateData(), MockObjWithTemplateData()]
        template_data_list = generator.process_template_data_list(objects_with_template, 'ja')
        assert len(template_data_list) == 2
        assert all(data['lang'] == 'ja' for data in template_data_list)
    
    def test_enhanced_validation_in_mock_generators(self):
        """Test that mock generators can use enhanced validation."""
        
        class EnhancedMockListGenerator(MockListBasedGenerator):
            def validate_data(self, data: Dict[str, Any]) -> bool:
                """Enhanced validation using ValidationMixin."""
                return (self.validate_required_fields(data, ['filename', 'content']) and
                        self.validate_string_field(data, 'filename'))
        
        generator = EnhancedMockListGenerator('ja', ['item1'])
        results = list(generator.generate())
        
        # Should pass validation with proper data
        assert len(results) == 1
        assert results[0]['filename'] == 'item1.rst'
        
        # Test with invalid data
        generator_invalid = EnhancedMockListGenerator('ja', ['item1'])
        generator_invalid.process_item = Mock(return_value={'filename': '', 'content': 'test'})
        
        results_invalid = list(generator_invalid.generate())
        # Should fail validation due to empty filename
        assert len(results_invalid) == 0
