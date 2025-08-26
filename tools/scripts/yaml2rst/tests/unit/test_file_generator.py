"""Unit tests for the file generator module."""
import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import logging

from yaml2rst.generators.file_generator import FileGenerator, GeneratorConfig
from yaml2rst.generators.base_generator import BaseGenerator, GeneratorError
from yaml2rst.generators.mixins import ValidationMixin


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

    @pytest.mark.parametrize(
        "template_name,output_path,should_raise,expected_error", [
            ('', '/test/output', True, "Template name must not be empty"),
            ('test_template', '', True, "Output path must not be empty"),
            ('test_template', '/test/output', False, None),
        ])
    def test_generator_config_validation(self, mock_generator_class,
                                         template_name, output_path,
                                         should_raise, expected_error):
        """Test GeneratorConfig validation with various parameters."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name=template_name,
            output_path=output_path
        )

        if should_raise:
            with pytest.raises(ValueError, match=expected_error):
                config.validate()
        else:
            # Should not raise any exception
            config.validate()

    def test_generator_config_validation_missing_required_fields(
            self, mock_generator_class):
        """Test GeneratorConfig validation when required fields validation
        fails."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output'
        )

        # Mock ValidationMixin.validate_required_fields to return False
        with patch('yaml2rst.generators.mixins.ValidationMixin.'
                   'validate_required_fields', return_value=False):
            with pytest.raises(ValueError,
                               match="Required configuration fields are "
                                     "missing"):
                config.validate()


class TestFileGenerator:
    """Test cases for FileGenerator class."""

    def test_file_generator_initialization(self, mock_templates):
        """Test FileGenerator initialization."""
        generator = FileGenerator(mock_templates, 'ja')

        assert generator.templates == mock_templates
        assert generator.lang == 'ja'
        assert isinstance(generator.logger, logging.Logger)

    def test_generate_success_single_file(self, mock_templates,
                                          mock_generator_class):
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

    def test_generate_success_multiple_files(self, mock_templates,
                                             mock_generator_class, temp_dir):
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

    def test_generate_with_extra_args(self, mock_templates,
                                      mock_generator_class):
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
        mock_generator_class.assert_called_once_with(
            **{'lang': 'ja', **extra_args})

    def test_generate_template_not_found(self, mock_templates,
                                         mock_generator_class):
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
        with pytest.raises(GeneratorError,
                           match="Template not found: nonexistent_template"):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_invalid_config(self, mock_templates,
                                     mock_generator_class):
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

    def test_generate_generator_exception(self, mock_templates,
                                          mock_generator_class):
        """Test generation when generator raises exception."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')

        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.side_effect = Exception(
            "Generator failed")

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )

        # Execute and verify
        with pytest.raises(GeneratorError,
                           match="Failed to generate files"):
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

        with pytest.raises(GeneratorError,
                           match="Failed to create directory"):
            generator._ensure_directory(test_path)

    @pytest.mark.parametrize(
        "is_single_file,output_path,filename,expected_result", [
            (True, '/test/output.rst', 'ignored', '/test/output.rst'),
            (False, '/test/output', 'test_file', '/test/output/test_file.rst'),
        ])
    def test_determine_destination(self, mock_templates, mock_generator_class,
                                   is_single_file, output_path, filename,
                                   expected_result):
        """Test destination determination for single and multiple files."""
        generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path=output_path,
            is_single_file=is_single_file
        )

        output_path_obj = Path(output_path)
        data = {'filename': filename}

        result = generator._determine_destination(config, output_path_obj,
                                                  data)

        assert result == Path(expected_result)

    @pytest.mark.parametrize(
        "build_all,targets,dest_path,is_single_file,expected_result", [
            (True, [], '/test/output.rst', True, True),
            (False, ['/test/output.rst'], '/test/output.rst', True, True),
            (False, ['/test/output'], '/test/output/file.rst', False, True),
            (False, ['/other/file.rst'], '/test/output.rst', True, False),
        ])
    def test_should_generate(self, mock_templates, mock_generator_class,
                             build_all, targets, dest_path, is_single_file,
                             expected_result):
        """Test should_generate logic with various scenarios."""
        generator = FileGenerator(mock_templates, 'ja')

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output.rst',
            is_single_file=is_single_file
        )

        result = generator._should_generate(
            config, build_all=build_all, targets=targets,
            dest_path=Path(dest_path)
        )

        assert result is expected_result


class TestFileGeneratorIntegration:
    """Integration tests for FileGenerator."""

    def test_full_generation_workflow(self, mock_templates, temp_dir):
        """Test complete generation workflow."""
        # Create a real generator class for testing
        class TestGenerator(BaseGenerator):
            def generate(self):
                yield {'filename': 'test1', 'title': 'Test 1',
                       'content': 'Content 1'}
                yield {'filename': 'test2', 'title': 'Test 2',
                       'content': 'Content 2'}

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
                yield {'filename': 'target_file',
                       'content': 'Target content'}
                yield {'filename': 'other_file',
                       'content': 'Other content'}

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
        generator.generate(config, build_all=False,
                           targets=[target_path])

        # Verify only one file was generated
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 1

        # Check that the correct file was generated
        call_args = template.write_rst.call_args[0]
        assert call_args[0]['filename'] == 'target_file'


class TestGeneratorConfigValidationMixin:
    """Test ValidationMixin integration in GeneratorConfig."""

    def test_generator_config_inherits_validation_mixin(
            self, mock_generator_class):
        """Test that GeneratorConfig inherits from ValidationMixin."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output'
        )

        # Should be instance of ValidationMixin
        assert isinstance(config, ValidationMixin)

        # Should have ValidationMixin methods
        assert hasattr(config, 'validate_required_fields')
        assert hasattr(config, 'validate_string_field')
        assert hasattr(config, 'validate_list_field')

    def test_generator_config_validation_with_whitespace_template(
            self, mock_generator_class):
        """Test GeneratorConfig validation with whitespace-only template
        name."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='   ',  # Whitespace only
            output_path='/test/output'
        )

        with pytest.raises(ValueError,
                           match="Template name must not be empty"):
            config.validate()

    def test_generator_config_validation_with_whitespace_output_path(
            self, mock_generator_class):
        """Test GeneratorConfig validation with whitespace-only output
        path."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='   '  # Whitespace only
        )

        with pytest.raises(ValueError,
                           match="Output path must not be empty"):
            config.validate()

    def test_generator_config_validation_enhanced_error_handling(
            self, mock_generator_class):
        """Test enhanced validation error handling."""
        # Test with None values (should be caught by ValidationMixin)
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name=None,
            output_path='/test/output'
        )

        with pytest.raises(ValueError):
            config.validate()

    def test_generator_config_validation_mixin_methods_work(
            self, mock_generator_class):
        """Test that ValidationMixin methods work correctly in
        GeneratorConfig."""
        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='test_template',
            output_path='/test/output'
        )

        # Test validate_required_fields
        test_data = {'template_name': 'test', 'output_path': '/path'}
        assert config.validate_required_fields(
            test_data, ['template_name', 'output_path']) is True
        assert config.validate_required_fields(
            test_data, ['template_name', 'missing']) is False

        # Test validate_string_field
        assert config.validate_string_field(
            test_data, 'template_name') is True
        assert config.validate_string_field(
            test_data, 'missing_field') is False

        # Test with empty string
        empty_data = {'template_name': '', 'output_path': '/path'}
        assert config.validate_string_field(
            empty_data, 'template_name', allow_empty=True) is True
        assert config.validate_string_field(
            empty_data, 'template_name', allow_empty=False) is False


class TestFileGeneratorEnhancedErrorHandling:
    """Test enhanced error handling in FileGenerator."""

    def test_generate_with_template_write_error(self, mock_templates,
                                                mock_generator_class):
        """Test generation when template.write_rst raises exception."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')

        mock_data = {'filename': 'test', 'content': 'test content'}
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = [mock_data]

        # Make template.write_rst raise an exception
        template = mock_templates['category_page']
        template.write_rst.side_effect = Exception(
            "Template write failed")

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )

        # Execute and verify
        with pytest.raises(GeneratorError,
                           match="File generation failed"):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_with_generator_instantiation_error(
            self, mock_templates, mock_generator_class):
        """Test generation when generator instantiation fails."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')

        # Make generator class raise exception during instantiation
        mock_generator_class.side_effect = Exception(
            "Generator instantiation failed")

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )

        # Execute and verify
        with pytest.raises(GeneratorError,
                           match="Failed to generate files"):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_with_data_processing_error(self, mock_templates,
                                                 mock_generator_class,
                                                 temp_dir):
        """Test generation when data processing fails."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')

        # Generator returns data without 'filename' key for multiple files
        mock_data = {'content': 'test content'}  # Missing 'filename'
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = [mock_data]

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path=str(temp_dir),  # Use temp_dir
            is_single_file=False  # This will try to access data['filename']
        )

        # Execute and verify
        with pytest.raises(GeneratorError,
                           match="File generation failed"):
            generator.generate(config, build_all=True, targets=[])

    def test_generate_logging_behavior(self, mock_templates,
                                       mock_generator_class):
        """Test that FileGenerator logs appropriately."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        generator.logger = Mock()

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

        # Verify logging calls
        assert generator.logger.info.call_count >= 2

        # Check specific log messages
        log_calls = [call[0][0] for call in
                     generator.logger.info.call_args_list]
        assert any("Starting generation" in msg for msg in log_calls)
        assert any("Processing destination" in msg for msg in log_calls)
        assert any("Generating file" in msg for msg in log_calls)

    def test_generate_skipping_behavior_logging(self, mock_templates,
                                                mock_generator_class):
        """Test logging when files are skipped."""
        # Setup
        generator = FileGenerator(mock_templates, 'ja')
        generator.logger = Mock()

        mock_data = {'filename': 'test', 'content': 'test content'}
        mock_generator_instance = mock_generator_class.return_value
        mock_generator_instance.generate.return_value = [mock_data]

        config = GeneratorConfig(
            generator_class=mock_generator_class,
            template_name='category_page',
            output_path='/test/output.rst',
            is_single_file=True
        )

        # Execute with build_all=False and no matching targets
        generator.generate(config, build_all=False,
                           targets=['/other/file.rst'])
        # Execute with build_all=False and no matching targets
        generator.generate(config, build_all=False,
                           targets=['/other/file.rst'])

        # Verify skipping was logged
        log_calls = [call[0][0] for call in
                     generator.logger.info.call_args_list]
        assert any("Skipping file" in msg for msg in log_calls)

        # Verify template.write_rst was not called
        template = mock_templates['category_page']
        template.write_rst.assert_not_called()
