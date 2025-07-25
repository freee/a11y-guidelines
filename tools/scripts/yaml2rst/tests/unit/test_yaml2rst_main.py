"""Unit tests for the main yaml2rst module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst import yaml2rst
from yaml2rst.generators.file_generator import GeneratorConfig


class TestMain:
    """Test cases for the main() function."""

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_main_successful_execution(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings,
        sample_dest_dirs,
        sample_static_files,
        mock_templates
    ):
        """Test successful execution of main function."""
        # Setup mocks
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (
            sample_dest_dirs,
            sample_static_files,
            {'test_var': 'test_value'}
        )
        mock_initializer.setup_templates.return_value = mock_templates
        mock_initializer.setup_variables.return_value = ({}, {})
        
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        # Execute
        yaml2rst.main()
        
        # Verify initialization calls
        mock_initializer.setup_parameters.assert_called_once()
        mock_initializer.setup_constants.assert_called_once_with(sample_settings)
        mock_initializer.setup_templates.assert_called_once()
        mock_initializer.setup_variables.assert_called_once()
        
        # Verify Config initialization
        mock_config.initialize.assert_called_once_with(
            profile="yaml2rst",
            config_override={
                "basedir": sample_settings['basedir'],
                "languages": {
                    "default": sample_settings['lang']
                }
            }
        )
        
        # Verify setup_instances call
        mock_setup_instances.assert_called_once_with(sample_settings['basedir'])
        
        # Verify directory creation
        assert mock_makedirs.call_count == len(sample_dest_dirs)
        
        # Verify FileGenerator creation
        mock_file_generator_class.assert_called_once_with(mock_templates, sample_settings['lang'])
        
        # Verify generator calls (should be called for each generator config)
        assert mock_file_generator.generate.call_count >= 10  # At least 10 generators

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    def test_main_config_initialization_error(
        self,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings
    ):
        """Test main function when Config initialization fails."""
        # Setup mocks
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (
            {
                'guidelines': '/test/guidelines',
                'checks': '/test/checks',
                'misc': '/test/misc',
                'info2gl': '/test/info2gl',
                'info2faq': '/test/info2faq',
                'faq_base': '/test/faq',
                'faq_articles': '/test/faq/articles',
                'faq_tags': '/test/faq/tags'
            },
            {
                'all_checks': '/test/all_checks.rst',
                'wcag21mapping': '/test/wcag21mapping.rst',
                'priority_diff': '/test/priority_diff.rst',
                'miscdefs': '/test/miscdefs.txt',
                'faq_index': '/test/faq_index.rst',
                'faq_tag_index': '/test/faq_tag_index.rst',
                'faq_article_index': '/test/faq_article_index.rst',
                'makefile': '/test/Makefile',
                'axe_rules': '/test/axe_rules.rst'
            },
            {}
        )
        mock_initializer.setup_templates.return_value = {}
        mock_initializer.setup_variables.return_value = ({}, {})
        
        mock_config.initialize.side_effect = Exception("Config initialization failed")
        
        # Execute and verify exception
        with pytest.raises(Exception, match="Config initialization failed"):
            yaml2rst.main()

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    @patch('os.makedirs')
    def test_main_directory_creation_error(
        self,
        mock_makedirs,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings,
        sample_dest_dirs
    ):
        """Test main function when directory creation fails."""
        # Setup mocks
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (sample_dest_dirs, {}, {})
        mock_initializer.setup_templates.return_value = {}
        mock_initializer.setup_variables.return_value = ({}, {})
        
        mock_makedirs.side_effect = OSError("Permission denied")
        
        # Execute and verify exception
        with pytest.raises(OSError, match="Permission denied"):
            yaml2rst.main()

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_main_file_generation_error(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings,
        mock_templates
    ):
        """Test main function when file generation fails."""
        # Setup mocks
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (
            {
                'guidelines': '/test/guidelines',
                'checks': '/test/checks',
                'faq_articles': '/test/faq',
                'faq_tags': '/test/faq/tags',
                'info2gl': '/test/info',
                'info2faq': '/test/info'
            },
            {
                'all_checks': '/test/all_checks.rst',
                'faq_index': '/test/faq/index.rst',
                'faq_tag_index': '/test/faq/tags/index.rst',
                'faq_article_index': '/test/faq/articles/index.rst',
                'wcag21mapping': '/test/info/wcag21-mapping.rst',
                'priority_diff': '/test/info/priority.rst',
                'miscdefs': '/test/inc/miscdefs.txt',
                'axe_rules': '/test/info/axe-rules.rst',
                'makefile': '/test/Makefile'
            },
            {}
        )
        mock_initializer.setup_templates.return_value = mock_templates
        mock_initializer.setup_variables.return_value = ({}, {})
        
        mock_file_generator = Mock()
        mock_file_generator.generate.side_effect = Exception("File generation failed")
        mock_file_generator_class.return_value = mock_file_generator
        
        # Execute and verify exception
        with pytest.raises(Exception, match="File generation failed"):
            yaml2rst.main()

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_main_generator_configurations(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings,
        sample_dest_dirs,
        sample_static_files,
        mock_templates
    ):
        """Test that all expected generators are configured correctly."""
        # Setup mocks
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (
            sample_dest_dirs,
            sample_static_files,
            {'test_var': 'test_value'}
        )
        mock_initializer.setup_templates.return_value = mock_templates
        mock_initializer.setup_variables.return_value = ({}, {})
        
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        # Execute
        yaml2rst.main()
        
        # Verify generator configurations
        generate_calls = mock_file_generator.generate.call_args_list
        
        # Check that we have the expected number of generator calls
        assert len(generate_calls) >= 12  # At least 12 generators including makefile
        
        # Verify specific generator types are present
        config_args = [call[0][0] for call in generate_calls]
        
        # Check for key generator classes
        generator_classes = [config.generator_class.__name__ for config in config_args]
        
        expected_generators = [
            'CategoryGenerator',
            'AllChecksGenerator',
            'CheckExampleGenerator',
            'FaqArticleGenerator',
            'FaqTagPageGenerator',
            'FaqIndexGenerator',
            'WcagMappingGenerator',
            'MakefileGenerator'
        ]
        
        for expected in expected_generators:
            assert any(expected in gen_class for gen_class in generator_classes), \
                f"Expected generator {expected} not found in {generator_classes}"

    @patch('yaml2rst.yaml2rst.initializer')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_main_makefile_generation(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_config,
        mock_setup_instances,
        mock_initializer,
        sample_settings,
        sample_dest_dirs,
        sample_static_files,
        mock_templates
    ):
        """Test that Makefile generation is handled correctly."""
        # Setup mocks
        makefile_vars = {'test_var': 'test_value'}
        mock_initializer.setup_parameters.return_value = sample_settings
        mock_initializer.setup_constants.return_value = (
            sample_dest_dirs,
            sample_static_files,
            makefile_vars
        )
        mock_initializer.setup_templates.return_value = mock_templates
        mock_initializer.setup_variables.return_value = ({'var1': 'val1'}, {'list1': []})
        
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        # Execute
        yaml2rst.main()
        
        # Verify Makefile generator was called
        generate_calls = mock_file_generator.generate.call_args_list
        
        # Find the Makefile generator call
        makefile_calls = [
            call for call in generate_calls
            if call[0][0].generator_class.__name__ == 'MakefileGenerator'
        ]
        
        assert len(makefile_calls) == 1, "Makefile generator should be called exactly once"
        
        # Verify the Makefile generator config
        makefile_config = makefile_calls[0][0][0]
        assert makefile_config.template_name == 'makefile'
        assert makefile_config.is_single_file is True
        assert 'config' in makefile_config.extra_args


class TestMainIntegration:
    """Integration tests for main function with real components."""

    def test_main_with_minimal_setup(self, temp_dir, monkeypatch):
        """Test main function with minimal real setup."""
        # Create minimal directory structure
        data_dir = temp_dir / "data"
        data_dir.mkdir()
        
        # Mock sys.argv to provide test arguments
        test_args = ['yaml2rst', '--basedir', str(temp_dir), '--lang', 'ja']
        monkeypatch.setattr('sys.argv', test_args)
        
        # Mock the freee_a11y_gl dependencies
        mock_config = Mock()
        mock_setup = Mock()
        
        with patch('yaml2rst.yaml2rst.Config', mock_config), \
             patch('yaml2rst.yaml2rst.setup_instances', mock_setup), \
             patch('yaml2rst.yaml2rst.FileGenerator') as mock_fg:
            
            mock_file_generator = Mock()
            mock_fg.return_value = mock_file_generator
            
            # This should not raise an exception
            yaml2rst.main()
            
            # Verify basic initialization occurred
            mock_config.initialize.assert_called_once()
            mock_setup.assert_called_once()
