"""Unit tests for the file generator module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst.generators.file_generator import FileGenerator, GeneratorConfig
from yaml2rst.generators.base_generator import BaseGenerator, GeneratorError


class TestGeneratorConfig:
    """Test cases for GeneratorConfig dataclass."""

    def test_generator_config_creation(self, mock_generator_class):
        """Test GeneratorConfig creation with valid parameters."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output',
            is_single_file=True,
            extra_args={'arg1': 'value1'}
        )
        
        assert config.generator_class == mock_generator_class
        assert config.template_name == 'test_template'
        assert config.output_path == '/test/output'
        assert config.is_single_file is True
        assert config.extra_args == {'arg1': 'value1'}

    def test_generator_config_defaults(self, mock_generator_class):
        """Test GeneratorConfig with default values."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output'
        )
        
        assert config.is_single_file is False
        assert config.extra_args is None

    def test_generator_config_validation_empty_template(self, mock_generator_class):
        """Test GeneratorConfig validation with empty template name."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='',
            output_path='/test/output'
        )
        
        with pytest.raises(ValueError, match="Template name must not be empty"):
            config.validate()

    def test_generator_config_validation_empty_output_path(self, mock_generator_class):
        """Test GeneratorConfig validation with empty output path."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path=''
        )
        
        with pytest.raises(ValueError, match="Output path must not be empty"):
            config.validate()

    def test_generator_config_validation_success(self, mock_generator_class):
        """Test GeneratorConfig validation with valid parameters."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output'
        )
        
        # Should not raise any exception
        config.validate()


class TestFileGenerator:
    """Test cases for FileGenerator class."""

    def test_file_generator_initialization(self, mock_templates):
        """Test FileGenerator initialization."""
        generator = FileGenerator(mock_templates, 'ja')
        
        assert generator.templates == mock_templates
        assert generator.lang == 'ja'
        assert isinstance(generator.logger, logging.Logger)

    def test_generate_success_single_file(self, mock_templates, mock_generator_class):
        """Test successful generation for single file."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        mock_data = {'filename': 'test', 'content': 'test content'}
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = [mock_data]
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        # Execute
        generator.generate(config, build_all=True, targets=[])
        
        # Verify
        mock_generator_class.assert_called_once_with('ja')
        mock_generator_instance.generate.assert_called_once()
        
        template = mock_templates['category_page']
        template.write_rst.assert_called_once()
        
        # Check that lang was added to data
        call_args = template.write_rst.call_args[0]
        assert call_args[0]['lang'] == 'ja'

    def test_generate_success_multiple_files(self, mock_templates, mock_generator_class, temp_dir):
        """Test successful generation for multiple files."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        mock_data_list = [
            {'filename': 'test1', 'content': 'content1'},
            {'filename': 'test2', 'content': 'content2'}
        ]
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = mock_data_list
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )
        
        # Execute
        generator.generate(config, build_all=True, targets=[])
        
        # Verify
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 2

    def test_generate_with_extra_args(self, mock_templates, mock_generator_class):
        """Test generation with extra arguments."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        mock_data = {'filename': 'test', 'content': 'test content'}
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = [mock_data]
        
        extra_args = {'config': {'key': 'value'}}
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True,
            extra_args=extra_args
        )
        
        # Execute
        generator.generate(config, build_all=True, targets=[])
        
        # Verify generator was called with extra args
        mock_generator_class.assert_called_once_with(**{'lang': 'ja', **extra_args})

    def test_generate_template_not_found(self, mock_templates, mock_generator_class):
        """Test generation when template is not found."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='nonexistent_template',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        # Execute and verify
        with pytest.raises(GeneratorError, match="Template not found: nonexistent_template"):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_invalid_config(self, mock_templates, mock_generator_class):
        """Test generation with invalid config."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='',  # Invalid empty template name
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        # Execute and verify
        with pytest.raises(GeneratorError):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_generator_exception(self, mock_templates, mock_generator_class):
        """Test generation when generator raises exception."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.side_effect = Exception("Generator failed")
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        # Execute and verify
        with pytest.raises(GeneratorError, match="Failed to generate files"):
            generator.generate(config, build_all=True, targets=[])

    @patch('pathlib.Path.mkdir')
    def test_ensure_directory_success(self, mock_mkdir, mock_templates):
        """Test successful directory creation."""
        generator = FileGenerator(mock_templates, 'ja')
        test_path = Path('/test/path')
        
        generator._ensure_directory(test_path)
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch('pathlib.Path.mkdir')
    def test_ensure_directory_failure(self, mock_mkdir, mock_templates):
        """Test directory creation failure."""
        generator = FileGenerator(mock_templates, 'ja')
        test_path = Path('/test/path')
        
        mock_mkdir.side_effect = OSError("Permission denied")
        
        with pytest.raises(GeneratorError, match="Failed to create directory"):
            generator._ensure_directory(test_path)

    def test_determine_destination_single_file(self, mock_templates, mock_generator_class):
        """Test destination determination for single file."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        output_path = Path('/test/output.rst')
        data = {'filename': 'ignored'}
        
        result = generator._determine_destination(config, output_path, data)
        
        assert result == output_path

    def test_determine_destination_multiple_files(self, mock_templates, mock_generator_class):
        """Test destination determination for multiple files."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output',
            is_single_file=False
        )
        
        output_path = Path('/test/output')
        data = {'filename': 'test_file'}
        
        result = generator._determine_destination(config, output_path, data)
        
        expected = output_path / 'test_file.rst'
        assert result == expected

    def test_should_generate_build_all(self, mock_templates, mock_generator_class):
        """Test should_generate when build_all is True."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        result = generator._should_generate(
            config, build_all=True, targets=[], dest_path=Path('/test/output.rst')
        )
        
        assert result is True

    def test_should_generate_specific_target(self, mock_templates, mock_generator_class):
        """Test should_generate when file is in targets."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        dest_path = Path('/test/output.rst')
        targets = [str(dest_path)]
        
        result = generator._should_generate(
            config, build_all=False, targets=targets, dest_path=dest_path
        )
        
        assert result is True

    def test_should_generate_parent_directory_target(self, mock_templates, mock_generator_class):
        """Test should_generate when parent directory is in targets."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output',
            is_single_file=False
        )
        
        dest_path = Path('/test/output/file.rst')
        targets = ['/test/output']
        
        result = generator._should_generate(
            config, build_all=False, targets=targets, dest_path=dest_path
        )
        
        assert result is True

    def test_should_generate_no_match(self, mock_templates, mock_generator_class):
        """Test should_generate when no match found."""
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output.rst',
            is_single_file=True
        )
        
        dest_path = Path('/test/output.rst')
        targets = ['/other/file.rst']
        
        result = generator._should_generate(
            config, build_all=False, targets=targets, dest_path=dest_path
        )
        
        assert result is False


class TestFileGeneratorIntegration:
    """Integration tests for FileGenerator."""

    def test_full_generation_workflow(self, mock_templates, temp_dir):
        """Test complete generation workflow."""
        # Create a real generator class for testing
        class TestGenerator(BaseGenerator):
            def generate(self):
                yield {'filename': 'test1', 'title': 'Test 1', 'content': 'Content 1'}
                yield {'filename': 'test2', 'title': 'Test 2', 'content': 'Content 2'}
        
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=TestGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )
        
        # Execute
        generator.generate(config, build_all=True, targets=[])
        
        # Verify
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 2
        
        # Check that data was processed correctly
        calls = template.write_rst.call_args_list
        for call in calls:
            data, path = call[0]
            assert 'lang' in data
            assert data['lang'] == 'ja'
            assert isinstance(path, Path)
            assert path.suffix == '.rst'

    def test_selective_generation(self, mock_templates, temp_dir):
        """Test selective file generation based on targets."""
        # Create a real generator class for testing
        class TestGenerator(BaseGenerator):
            def generate(self):
                yield {'filename': 'target_file', 'content': 'Target content'}
                yield {'filename': 'other_file', 'content': 'Other content'}
        
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=TestGenerator,
            template_name='category_page',
            output_path=str(temp_dir),
            is_single_file=False
        )
        
        # Target only one file
        target_path = str(temp_dir / 'target_file.rst')
        
        # Execute
        generator.generate(config, build_all=False, targets=[target_path])
        
        # Verify only one file was generated
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 1
        
        # Check that the correct file was generated
        call_args = template.write_rst.call_args[0]
        assert call_args[0]['filename'] == 'target_file'
