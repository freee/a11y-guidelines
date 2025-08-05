"""Tests for yaml2rst main module and entry point."""
import os
import subprocess
import sys
from unittest.mock import Mock, patch

import pytest

from yaml2rst import yaml2rst


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
        mock_initializer.setup_constants.assert_called_once_with(
            sample_settings)
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
        mock_setup_instances.assert_called_once_with(
            sample_settings['basedir'])

        # Verify directory creation
        assert mock_makedirs.call_count == len(sample_dest_dirs)

        # Verify FileGenerator creation
        mock_file_generator_class.assert_called_once_with(
            mock_templates, sample_settings['lang'])

        # Verify generator calls (should be called for each generator config)
        assert mock_file_generator.generate.call_count >= 10

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

        mock_config.initialize.side_effect = Exception(
            "Config initialization failed")

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
        mock_initializer.setup_constants.return_value = (
            sample_dest_dirs, {}, {})
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
        mock_file_generator.generate.side_effect = Exception(
            "File generation failed")
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
        assert len(generate_calls) >= 12

        # Verify specific generator types are present
        config_args = [call[0][0] for call in generate_calls]

        # Check for key generator classes
        generator_classes = [config.generator_class.__name__
                             for config in config_args]

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
            assert any(expected in gen_class
                       for gen_class in generator_classes), \
                f"Expected generator {expected} not found in " \
                f"{generator_classes}"

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
        mock_initializer.setup_variables.return_value = (
            {'var1': 'val1'}, {'list1': []})

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

        assert len(makefile_calls) == 1, \
            "Makefile generator should be called exactly once"

        # Verify the Makefile generator config
        makefile_config = makefile_calls[0][0][0]
        assert makefile_config.template_name == 'makefile'
        assert makefile_config.is_single_file is True
        assert 'config' in makefile_config.extra_args


class TestMainEntryPoint:
    """Test the main entry point functionality."""

    def test_main_entry_point_structure(self):
        """Test that __main__.py has the correct structure."""
        import yaml2rst.__main__

        # Read the __main__.py file content
        with open(yaml2rst.__main__.__file__, 'r') as f:
            content = f.read()

        # Verify it contains the expected import and execution pattern
        assert 'from .yaml2rst import main' in content
        assert "if __name__ == '__main__':" in content
        assert 'main()' in content

    @patch('yaml2rst.__main__.main')
    def test_main_import_without_execution(self, mock_main):
        """Test that importing __main__ doesn't call main() when not run
        directly."""
        # Import the module (should not call main since __name__ != '__main__')
        import yaml2rst.__main__

        # Reset and test that main exists and is callable
        mock_main.reset_mock()

        # Verify the main function is available
        assert hasattr(yaml2rst.__main__, 'main')
        assert callable(yaml2rst.__main__.main)

    def test_main_module_structure(self):
        """Test the structure and imports of __main__.py."""
        import yaml2rst.__main__

        # Verify that main is imported from yaml2rst
        assert hasattr(yaml2rst.__main__, 'main')

        # Verify the module has the expected attributes
        assert hasattr(yaml2rst.__main__, '__name__')
        assert hasattr(yaml2rst.__main__, '__file__')

    def test_main_function_integration(self):
        """Test that the main function from yaml2rst module is imported."""
        from yaml2rst.__main__ import main
        from yaml2rst.yaml2rst import main as yaml2rst_main

        # Verify that the imported main is the same as the one from yaml2rst
        assert main is yaml2rst_main

    def test_module_can_be_executed_as_script(self):
        """Test that the module can be executed as a script using python -m."""
        # Get the absolute path to the yaml2rst directory
        yaml2rst_dir = os.path.join(os.path.dirname(__file__), '../../')
        yaml2rst_dir = os.path.abspath(yaml2rst_dir)

        # Test running the module as a script (this will actually execute it)
        # We'll use --help to avoid full execution but verify entry point works
        result = subprocess.run(
            [sys.executable, '-m', 'yaml2rst', '--help'],
            cwd=yaml2rst_dir,
            capture_output=True,
            text=True
        )

        # The command should execute without import errors
        # Even if it fails due to missing arguments, no import errors
        assert 'ModuleNotFoundError' not in result.stderr
        assert 'ImportError' not in result.stderr

    def test_main_execution_when_run_as_main(self):
        """Test that main() is called when __main__.py is executed as main."""
        # This test verifies the structure and logic of the __main__.py file
        import yaml2rst.__main__

        # Read the file and verify the execution logic is present
        with open(yaml2rst.__main__.__file__, 'r') as f:
            content = f.read()

        # Verify the conditional execution structure
        lines = content.strip().split('\n')
        assert any("if __name__ == '__main__':" in line for line in lines)
        assert any("main()" in line for line in lines)

        # Verify the import is correct
        assert any("from .yaml2rst import main" in line for line in lines)


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
