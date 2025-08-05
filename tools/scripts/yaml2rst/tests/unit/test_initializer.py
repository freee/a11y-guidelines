"""Unit tests for the initializer module."""
import pytest
from unittest.mock import Mock, patch

from yaml2rst import initializer


class TestSetupParameters:
    """Test cases for setup_parameters function."""

    @patch('yaml2rst.initializer.parse_args')
    @patch('yaml2rst.initializer.process_arguments')
    def test_setup_parameters_success(self, mock_process_args,
                                      mock_parse_args):
        """Test successful parameter setup."""
        mock_args = Mock()
        mock_parse_args.return_value = mock_args

        expected_settings = {
            'build_all': True,
            'targets': [],
            'lang': 'ja',
            'basedir': '/test/basedir'
        }
        mock_process_args.return_value = expected_settings

        result = initializer.setup_parameters()

        mock_parse_args.assert_called_once()
        mock_process_args.assert_called_once_with(mock_args)
        assert result == expected_settings


class TestSetupConstants:
    """Test cases for setup_constants function."""

    @patch('yaml2rst.initializer.get_dest_dirnames')
    @patch('yaml2rst.initializer.get_static_dest_files')
    @patch('yaml2rst.initializer.get_src_path')
    def test_setup_constants_success(self, mock_get_src_path,
                                     mock_get_static_dest_files,
                                     mock_get_dest_dirnames,
                                     sample_settings):
        """Test successful constants setup."""
        mock_dest_dirs = {
            'guidelines': '/test/guidelines',
            'checks': '/test/checks',
            'faq_articles': '/test/faq',
            'faq_tags': '/test/faq/tags',
            'info2gl': '/test/info',
            'info2faq': '/test/info'
        }
        mock_static_files = {
            'all_checks': '/test/all_checks.rst',
            'faq_index': '/test/faq/index.rst',
            'faq_tag_index': '/test/faq/tags/index.rst',
            'faq_article_index': '/test/faq/articles/index.rst',
            'wcag21mapping': '/test/info/wcag21-mapping.rst',
            'priority_diff': '/test/info/priority.rst',
            'miscdefs': '/test/inc/miscdefs.txt',
            'axe_rules': '/test/info/axe-rules.rst',
            'makefile': '/test/Makefile'
        }
        mock_src_path = {
            'wcag_sc': '/test/wcag_sc.json',
            'info': '/test/info.json'
        }

        mock_get_dest_dirnames.return_value = mock_dest_dirs
        mock_get_static_dest_files.return_value = mock_static_files
        mock_get_src_path.return_value = mock_src_path

        dest_dirs, static_files, makefile_vars = (
            initializer.setup_constants(sample_settings))

        # Verify function calls
        mock_get_dest_dirnames.assert_called_once_with(
            sample_settings['basedir'],
            sample_settings['lang']
        )
        mock_get_static_dest_files.assert_called_once_with(
            sample_settings['basedir'],
            sample_settings['lang']
        )
        mock_get_src_path.assert_called_once_with(sample_settings['basedir'])

        # Verify return values
        assert dest_dirs == mock_dest_dirs
        assert static_files == mock_static_files
        assert isinstance(makefile_vars, dict)
        assert 'wcag_sc' in makefile_vars
        assert 'info_src' in makefile_vars


class TestSetupVariables:
    """Test cases for setup_variables function."""

    def test_setup_variables_returns_correct_structure(self):
        """Test that setup_variables returns the correct structure."""
        makefile_vars, makefile_vars_list = initializer.setup_variables()

        # Check makefile_vars structure
        assert isinstance(makefile_vars, dict)
        expected_vars = ['gl_yaml', 'check_yaml', 'faq_yaml']
        for var in expected_vars:
            assert var in makefile_vars
            assert makefile_vars[var] == ''

        # Check makefile_vars_list structure
        assert isinstance(makefile_vars_list, dict)
        expected_lists = [
            'guideline_category_target',
            'check_example_target',
            'faq_article_target',
            'faq_tagpage_target',
            'info_to_gl_target',
            'info_to_faq_target'
        ]
        for var_list in expected_lists:
            assert var_list in makefile_vars_list
            assert isinstance(makefile_vars_list[var_list], list)
            assert len(makefile_vars_list[var_list]) == 0


class TestSetupTemplates:
    """Test cases for setup_templates function."""

    @patch('yaml2rst.initializer.TemplateManager')
    @patch('yaml2rst.initializer.TEMPLATE_DIR', '/test/templates')
    @patch('yaml2rst.initializer.TEMPLATE_FILENAMES')
    def test_setup_templates_success(self, mock_template_filenames,
                                     mock_template_manager_class):
        """Test successful template setup."""
        mock_template_filenames.items.return_value = [
            ('category_page', 'gl-category.rst'),
            ('faq_article', 'faq/article.rst')
        ]

        mock_template_manager = Mock()
        mock_template = Mock()
        mock_template_manager.load.return_value = mock_template
        mock_template_manager_class.from_config.return_value = \
            mock_template_manager

        result = initializer.setup_templates()

        # Verify TemplateManager.from_config was called for each template
        assert mock_template_manager_class.from_config.call_count == 2

        # Verify template loading
        assert mock_template_manager.load.call_count == 2

        # Verify result structure
        assert isinstance(result, dict)
        assert 'category_page' in result
        assert 'faq_article' in result


class TestParseArgs:
    """Test cases for parse_args function."""

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_parse_args_default_values(self, mock_get_languages):
        """Test parse_args with default values."""
        mock_get_languages.return_value = ['ja', 'en']

        with patch('sys.argv', ['yaml2rst']):
            args = initializer.parse_args()

        assert args.lang == 'ja'
        assert args.basedir == '..'
        assert args.files == []

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_parse_args_custom_values(self, mock_get_languages):
        """Test parse_args with custom values."""
        mock_get_languages.return_value = ['ja', 'en']

        test_argv = [
            'yaml2rst',
            '--lang', 'en',
            '--basedir', '/custom/basedir',
            'file1.yaml', 'file2.yaml'
        ]

        with patch('sys.argv', test_argv):
            args = initializer.parse_args()

        assert args.lang == 'en'
        assert args.basedir == '/custom/basedir'
        assert args.files == ['file1.yaml', 'file2.yaml']

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_parse_args_invalid_language(self, mock_get_languages):
        """Test parse_args with invalid language."""
        mock_get_languages.return_value = ['ja', 'en']

        test_argv = ['yaml2rst', '--lang', 'invalid']

        with patch('sys.argv', test_argv):
            with pytest.raises(SystemExit):
                initializer.parse_args()

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_parse_args_help(self, mock_get_languages):
        """Test parse_args help option."""
        mock_get_languages.return_value = ['ja', 'en']

        with patch('sys.argv', ['yaml2rst', '--help']):
            with pytest.raises(SystemExit):
                initializer.parse_args()


class TestProcessArguments:
    """Test cases for process_arguments function."""

    def test_process_arguments_build_all(self):
        """Test process_arguments when building all files."""
        mock_args = Mock()
        mock_args.basedir = '/test/basedir'
        mock_args.files = []
        mock_args.lang = 'ja'
        mock_args.template_dir = None

        with patch('os.path.abspath') as mock_abspath:
            mock_abspath.return_value = '/absolute/test/basedir'

            result = initializer.process_arguments(mock_args)

        assert result['build_all'] is True
        assert result['targets'] == []
        assert result['lang'] == 'ja'
        assert result['basedir'] == '/absolute/test/basedir'
        assert result['template_dir'] is None

    def test_process_arguments_specific_files(self):
        """Test process_arguments when building specific files."""
        mock_args = Mock()
        mock_args.basedir = '/test/basedir'
        mock_args.files = ['file1.yaml', 'file2.yaml']
        mock_args.lang = 'en'
        mock_args.template_dir = None

        with patch('os.path.abspath') as mock_abspath:
            mock_abspath.side_effect = [
                '/absolute/test/basedir',
                '/absolute/file1.yaml',
                '/absolute/file2.yaml'
            ]

            result = initializer.process_arguments(mock_args)

        assert result['build_all'] is False
        assert result['targets'] == ['/absolute/file1.yaml',
                                     '/absolute/file2.yaml']
        assert result['lang'] == 'en'
        assert result['basedir'] == '/absolute/test/basedir'
        assert result['template_dir'] is None

    def test_process_arguments_empty_files_list(self):
        """Test process_arguments with empty files list."""
        mock_args = Mock()
        mock_args.basedir = '/test/basedir'
        mock_args.files = []
        mock_args.lang = 'ja'
        mock_args.template_dir = None

        with patch('os.path.abspath') as mock_abspath:
            mock_abspath.return_value = '/absolute/test/basedir'

            result = initializer.process_arguments(mock_args)

        assert result['build_all'] is True
        assert result['targets'] == []
        assert result['template_dir'] is None


class TestInitializerIntegration:
    """Integration tests for initializer functions."""

    @patch('yaml2rst.initializer.config.get_available_languages')
    @patch('yaml2rst.initializer.get_dest_dirnames')
    @patch('yaml2rst.initializer.get_static_dest_files')
    @patch('freee_a11y_gl.source.get_src_path')
    @patch('yaml2rst.initializer.TemplateManager')
    @patch('yaml2rst.initializer.TEMPLATE_FILENAMES')
    def test_full_initialization_flow(
        self,
        mock_template_filenames,
        mock_template_manager_class,
        mock_get_src_path,
        mock_get_static_dest_files,
        mock_get_dest_dirnames,
        mock_get_languages
    ):
        """Test the full initialization flow."""
        # Setup mocks
        mock_get_languages.return_value = ['ja', 'en']
        mock_get_dest_dirnames.return_value = {
            'guidelines': '/test/guidelines'}
        mock_get_static_dest_files.return_value = {
            'all_checks': '/test/all_checks.rst',
            'wcag21mapping': '/test/wcag21mapping.rst',
            'priority_diff': '/test/priority_diff.rst',
            'miscdefs': '/test/miscdefs.txt',
            'faq_index': '/test/faq_index.rst',
            'faq_tag_index': '/test/faq_tag_index.rst',
            'faq_article_index': '/test/faq_article_index.rst',
            'makefile': '/test/Makefile',
            'axe_rules': '/test/axe_rules.rst'
        }
        mock_get_src_path.return_value = {'wcag_sc': '/test/wcag_sc.json',
                                          'info': '/test/info.json'}

        mock_template_filenames.items.return_value = [
            ('category_page', 'gl-category.rst')]
        mock_template_manager = Mock()
        mock_template_manager.load.return_value = Mock()
        mock_template_manager_class.return_value = mock_template_manager

        # Test with default arguments
        with patch('sys.argv', ['yaml2rst']):
            settings = initializer.setup_parameters()
            dest_dirs, static_files, makefile_vars = (
                initializer.setup_constants(settings))
            templates = initializer.setup_templates()
            vars_dict, vars_list = initializer.setup_variables()

        # Verify results
        assert settings['lang'] == 'ja'
        assert settings['build_all'] is True
        assert isinstance(dest_dirs, dict)
        assert isinstance(static_files, dict)
        assert isinstance(makefile_vars, dict)
        assert isinstance(templates, dict)
        assert isinstance(vars_dict, dict)
        assert isinstance(vars_list, dict)
