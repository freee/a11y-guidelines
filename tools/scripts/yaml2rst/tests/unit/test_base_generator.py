"""Unit tests for the base generator module."""
import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst.generators.base_generator import (
    BaseGenerator, GeneratorError, ValidationError, GeneratorContext
)


class TestGeneratorContext:
    """Test cases for GeneratorContext dataclass."""

    def test_generator_context_creation(self):
        """Test GeneratorContext creation."""
        context = GeneratorContext(
            lang='ja',
            base_dir=Path('/test/basedir')
        )
        
        assert context.lang == 'ja'
        assert context.base_dir == Path('/test/basedir')

    def test_generator_context_with_string_path(self):
        """Test GeneratorContext with string path."""
        context = GeneratorContext(
            lang='en',
            base_dir=Path('/test/basedir')
        )
        
        assert context.lang == 'en'
        assert isinstance(context.base_dir, Path)


class TestGeneratorError:
    """Test cases for GeneratorError exception."""

    def test_generator_error_creation(self):
        """Test GeneratorError creation."""
        error = GeneratorError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_validation_error_creation(self):
        """Test ValidationError creation."""
        error = ValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert isinstance(error, GeneratorError)
        assert isinstance(error, Exception)


class ConcreteGenerator(BaseGenerator):
    """Concrete implementation of BaseGenerator for testing."""
    
    def __init__(self, lang, base_dir=None, test_data=None):
        super().__init__(lang, base_dir)
        self.test_data = test_data or []
    
    def generate(self):
        """Generate test data."""
        for item in self.test_data:
            yield item


class TestBaseGenerator:
    """Test cases for BaseGenerator class."""

    def test_base_generator_initialization(self):
        """Test BaseGenerator initialization."""
        generator = ConcreteGenerator('ja', Path('/test/basedir'))
        
        assert generator.context.lang == 'ja'
        assert generator.context.base_dir == Path('/test/basedir')
        assert generator.lang == 'ja'  # Backward compatibility
        assert isinstance(generator.logger, logging.Logger)

    def test_base_generator_initialization_default_basedir(self):
        """Test BaseGenerator initialization with default base_dir."""
        with patch('pathlib.Path.cwd', return_value=Path('/current/dir')):
            generator = ConcreteGenerator('en')
        
        assert generator.context.lang == 'en'
        assert generator.context.base_dir == Path('/current/dir')

    def test_base_generator_initialization_string_basedir(self):
        """Test BaseGenerator initialization with string base_dir."""
        generator = ConcreteGenerator('ja', '/test/basedir')
        
        assert generator.context.base_dir == Path('/test/basedir')

    def test_generate_abstract_method(self):
        """Test that generate is abstract in BaseGenerator."""
        # This test verifies that BaseGenerator cannot be instantiated directly
        with pytest.raises(TypeError):
            BaseGenerator('ja')

    def test_generate_not_implemented_error(self):
        """Test that generate raises NotImplementedError when called directly."""
        # Create a minimal subclass that implements generate to call super()
        class IncompleteGenerator(BaseGenerator):
            def generate(self):
                # Call the parent's generate method which should raise NotImplementedError
                return super().generate()
        
        generator = IncompleteGenerator('ja')
        
        with pytest.raises(NotImplementedError, match="Subclasses must implement generate"):
            list(generator.generate())

    def test_concrete_generator_generate(self):
        """Test concrete generator implementation."""
        test_data = [
            {'filename': 'test1', 'content': 'content1'},
            {'filename': 'test2', 'content': 'content2'}
        ]
        generator = ConcreteGenerator('ja', test_data=test_data)
        
        results = list(generator.generate())
        
        assert len(results) == 2
        assert results[0] == {'filename': 'test1', 'content': 'content1'}
        assert results[1] == {'filename': 'test2', 'content': 'content2'}

    def test_get_dependencies_default(self):
        """Test default get_dependencies implementation."""
        generator = ConcreteGenerator('ja')
        
        dependencies = generator.get_dependencies()
        
        assert isinstance(dependencies, list)
        assert len(dependencies) == 0

    def test_validate_data_default(self):
        """Test default validate_data implementation."""
        generator = ConcreteGenerator('ja')
        
        result = generator.validate_data({'test': 'data'})
        
        assert result is True

    def test_preprocess_data_default(self):
        """Test default preprocess_data implementation."""
        generator = ConcreteGenerator('ja')
        test_data = {'test': 'data'}
        
        result = generator.preprocess_data(test_data)
        
        assert result == test_data
        assert result is test_data  # Should return the same object

    def test_postprocess_data_default(self):
        """Test default postprocess_data implementation."""
        generator = ConcreteGenerator('ja')
        test_data = {'test': 'data'}
        
        result = generator.postprocess_data(test_data)
        
        assert result == test_data
        assert result is test_data  # Should return the same object

    def test_cleanup_default(self):
        """Test default cleanup implementation."""
        generator = ConcreteGenerator('ja')
        
        # Should not raise any exception
        generator.cleanup()


class TestProcessSingleItem:
    """Test cases for process_single_item method."""

    def test_process_single_item_not_implemented(self):
        """Test process_single_item when _process_item is not implemented."""
        generator = ConcreteGenerator('ja')
        
        with pytest.raises(GeneratorError):
            generator.process_single_item({'test': 'item'})

    def test_process_item_not_implemented_error(self):
        """Test that _process_item raises NotImplementedError when called directly."""
        generator = ConcreteGenerator('ja')
        
        with pytest.raises(NotImplementedError, match="Implement this method if using process_single_item"):
            generator._process_item({'test': 'item'})

    def test_process_single_item_success(self):
        """Test successful process_single_item."""
        class TestGenerator(ConcreteGenerator):
            def _process_item(self, item):
                return {'processed': item['value'], 'filename': 'test'}
            
            def validate_data(self, data):
                return 'processed' in data
        
        generator = TestGenerator('ja')
        result = generator.process_single_item({'value': 'test_value'})
        
        assert result == {'processed': 'test_value', 'filename': 'test'}

    def test_process_single_item_with_preprocessing(self):
        """Test process_single_item with preprocessing."""
        class TestGenerator(ConcreteGenerator):
            def _process_item(self, item):
                return {'value': item['value'], 'filename': 'test'}
            
            def preprocess_data(self, data):
                data['preprocessed'] = True
                return data
            
            def postprocess_data(self, data):
                data['postprocessed'] = True
                return data
        
        generator = TestGenerator('ja')
        result = generator.process_single_item({'value': 'test_value'})
        
        assert result['value'] == 'test_value'
        assert result['preprocessed'] is True
        assert result['postprocessed'] is True

    def test_process_single_item_validation_failure(self):
        """Test process_single_item when validation fails."""
        class TestGenerator(ConcreteGenerator):
            def _process_item(self, item):
                return {'value': item['value'], 'filename': 'test'}
            
            def validate_data(self, data):
                raise ValidationError("Validation failed")
        
        generator = TestGenerator('ja')
        
        with pytest.raises(GeneratorError):
            generator.process_single_item({'value': 'test_value'})

    def test_process_single_item_no_data_generated(self):
        """Test process_single_item when no data is generated."""
        class TestGenerator(ConcreteGenerator):
            def _process_item(self, item):
                return None
        
        generator = TestGenerator('ja')
        result = generator.process_single_item({'value': 'test_value'})
        
        assert result == {}

    def test_process_single_item_processing_error(self):
        """Test process_single_item when processing raises exception."""
        class TestGenerator(ConcreteGenerator):
            def _process_item(self, item):
                raise ValueError("Processing failed")
        
        generator = TestGenerator('ja')
        
        with pytest.raises(GeneratorError, match="Failed to process item"):
            generator.process_single_item({'value': 'test_value'})


class TestContextManager:
    """Test cases for context manager functionality."""

    def test_context_manager_enter_exit(self):
        """Test context manager enter and exit."""
        generator = ConcreteGenerator('ja')
        
        with generator as ctx:
            assert ctx is generator
        
        # Should complete without error

    def test_context_manager_cleanup_called(self):
        """Test that cleanup is called on context manager exit."""
        class TestGenerator(ConcreteGenerator):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cleanup_called = False
            
            def cleanup(self):
                self.cleanup_called = True
        
        generator = TestGenerator('ja')
        
        with generator:
            assert generator.cleanup_called is False
        
        assert generator.cleanup_called is True

    def test_context_manager_cleanup_on_exception(self):
        """Test that cleanup is called even when exception occurs."""
        class TestGenerator(ConcreteGenerator):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cleanup_called = False
            
            def cleanup(self):
                self.cleanup_called = True
        
        generator = TestGenerator('ja')
        
        try:
            with generator:
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        assert generator.cleanup_called is True


class TestCustomValidation:
    """Test cases for custom validation implementations."""

    def test_custom_validation_success(self):
        """Test custom validation that passes."""
        class ValidatingGenerator(ConcreteGenerator):
            def validate_data(self, data):
                return 'required_field' in data and data['required_field'] is not None
        
        generator = ValidatingGenerator('ja')
        
        valid_data = {'required_field': 'value', 'other': 'data'}
        result = generator.validate_data(valid_data)
        
        assert result is True

    def test_custom_validation_failure(self):
        """Test custom validation that fails."""
        class ValidatingGenerator(ConcreteGenerator):
            def validate_data(self, data):
                return 'required_field' in data and data['required_field'] is not None
        
        generator = ValidatingGenerator('ja')
        
        invalid_data = {'other': 'data'}
        result = generator.validate_data(invalid_data)
        
        assert result is False

    def test_custom_validation_with_exception(self):
        """Test custom validation that raises ValidationError."""
        class ValidatingGenerator(ConcreteGenerator):
            def validate_data(self, data):
                if 'required_field' not in data:
                    raise ValidationError("Required field missing")
                return True
        
        generator = ValidatingGenerator('ja')
        
        with pytest.raises(ValidationError, match="Required field missing"):
            generator.validate_data({'other': 'data'})


class TestCustomPrePostProcessing:
    """Test cases for custom pre/post processing implementations."""

    def test_custom_preprocessing(self):
        """Test custom preprocessing implementation."""
        class ProcessingGenerator(ConcreteGenerator):
            def preprocess_data(self, data):
                processed = data.copy()
                processed['preprocessed_at'] = 'timestamp'
                processed['lang'] = self.lang
                return processed
        
        generator = ProcessingGenerator('ja')
        original_data = {'title': 'Test Title'}
        
        result = generator.preprocess_data(original_data)
        
        assert result['title'] == 'Test Title'
        assert result['preprocessed_at'] == 'timestamp'
        assert result['lang'] == 'ja'
        assert original_data != result  # Should be a copy

    def test_custom_postprocessing(self):
        """Test custom postprocessing implementation."""
        class ProcessingGenerator(ConcreteGenerator):
            def postprocess_data(self, data):
                processed = data.copy()
                processed['postprocessed'] = True
                processed['final_check'] = len(data) > 0
                return processed
        
        generator = ProcessingGenerator('ja')
        original_data = {'title': 'Test Title', 'content': 'Test Content'}
        
        result = generator.postprocess_data(original_data)
        
        assert result['title'] == 'Test Title'
        assert result['content'] == 'Test Content'
        assert result['postprocessed'] is True
        assert result['final_check'] is True

    def test_chained_processing(self):
        """Test chained pre and post processing."""
        class ChainedGenerator(ConcreteGenerator):
            def preprocess_data(self, data):
                data['step'] = 1
                return data
            
            def postprocess_data(self, data):
                data['step'] = 2
                return data
            
            def _process_item(self, item):
                return {'original': item, 'filename': 'test'}
        
        generator = ChainedGenerator('ja')
        result = generator.process_single_item({'input': 'value'})
        
        assert result['original'] == {'input': 'value'}
        assert result['step'] == 2  # Should be postprocessed value
