"""Tests for common generators module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from yaml2rst.generators.common_generators import ListBasedGenerator, SingleFileGenerator


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
