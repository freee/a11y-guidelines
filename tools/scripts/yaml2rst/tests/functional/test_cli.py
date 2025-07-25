"""Functional tests for the CLI interface."""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import subprocess
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst import yaml2rst
from yaml2rst import initializer


class TestCLIInterface:
    """Test cases for command line interface."""

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_cli_default_arguments(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test CLI with default arguments."""
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        # Mock the initializer functions
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'base': str(temp_dir),
                'guidelines': str(temp_dir / 'categories'),
                'checks': str(temp_dir / 'checks'),
                'misc': str(temp_dir / 'misc'),
                'info2gl': str(temp_dir / 'info2gl'),
                'info2faq': str(temp_dir / 'info2faq'),
                'faq_base': str(temp_dir / 'faq'),
                'faq_articles': str(temp_dir / 'faq' / 'articles'),
                'faq_tags': str(temp_dir / 'faq' / 'tags')
            }
            mock_get_static.return_value = {
                'all_checks': str(temp_dir / 'checks' / 'allchecks.rst'),
                'wcag21mapping': str(temp_dir / 'misc' / 'wcag21-mapping.rst'),
                'priority_diff': str(temp_dir / 'misc' / 'priority-diff.rst'),
                'miscdefs': str(temp_dir / 'misc' / 'defs.txt'),
                'faq_index': str(temp_dir / 'faq' / 'index.rst'),
                'faq_article_index': str(temp_dir / 'faq' / 'articles' / 'index.rst'),
                'faq_tag_index': str(temp_dir / 'faq' / 'tags' / 'index.rst'),
                'makefile': str(temp_dir / 'incfiles.mk'),
                'axe_rules': str(temp_dir / 'misc' / 'axe-rules.rst')
            }
            mock_get_src.return_value = {'wcag_sc': str(temp_dir / 'wcag.json')}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            # Test with default arguments
            with patch('sys.argv', ['yaml2rst']):
                yaml2rst.main()
            
            # Verify default settings were used
            mock_config.initialize.assert_called_once()
            config_call = mock_config.initialize.call_args[1]
            assert config_call['config_override']['languages']['default'] == 'ja'

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_cli_custom_language(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test CLI with custom language argument."""
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'base': str(temp_dir),
                'guidelines': str(temp_dir / 'categories'),
                'checks': str(temp_dir / 'checks'),
                'misc': str(temp_dir / 'misc'),
                'info2gl': str(temp_dir / 'info2gl'),
                'info2faq': str(temp_dir / 'info2faq'),
                'faq_base': str(temp_dir / 'faq'),
                'faq_articles': str(temp_dir / 'faq' / 'articles'),
                'faq_tags': str(temp_dir / 'faq' / 'tags')
            }
            mock_get_static.return_value = {
                'all_checks': str(temp_dir / 'checks' / 'allchecks.rst'),
                'wcag21mapping': str(temp_dir / 'misc' / 'wcag21-mapping.rst'),
                'priority_diff': str(temp_dir / 'misc' / 'priority-diff.rst'),
                'miscdefs': str(temp_dir / 'misc' / 'defs.txt'),
                'faq_index': str(temp_dir / 'faq' / 'index.rst'),
                'faq_article_index': str(temp_dir / 'faq' / 'articles' / 'index.rst'),
                'faq_tag_index': str(temp_dir / 'faq' / 'tags' / 'index.rst'),
                'makefile': str(temp_dir / 'incfiles.mk'),
                'axe_rules': str(temp_dir / 'misc' / 'axe-rules.rst')
            }
            mock_get_src.return_value = {'wcag_sc': str(temp_dir / 'wcag.json')}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            # Test with English language
            with patch('sys.argv', ['yaml2rst', '--lang', 'en']):
                yaml2rst.main()
            
            # Verify English was used
            mock_config.initialize.assert_called_once()
            config_call = mock_config.initialize.call_args[1]
            assert config_call['config_override']['languages']['default'] == 'en'
            
            # Verify FileGenerator was created with English
            mock_file_generator_class.assert_called_once()
            generator_call = mock_file_generator_class.call_args[0]
            assert generator_call[1] == 'en'  # Second argument is language

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_cli_custom_basedir(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test CLI with custom base directory."""
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        custom_basedir = temp_dir / "custom_base"
        
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'base': str(temp_dir),
                'guidelines': str(temp_dir / 'categories'),
                'checks': str(temp_dir / 'checks'),
                'misc': str(temp_dir / 'misc'),
                'info2gl': str(temp_dir / 'info2gl'),
                'info2faq': str(temp_dir / 'info2faq'),
                'faq_base': str(temp_dir / 'faq'),
                'faq_articles': str(temp_dir / 'faq' / 'articles'),
                'faq_tags': str(temp_dir / 'faq' / 'tags')
            }
            mock_get_static.return_value = {
                'all_checks': str(temp_dir / 'checks' / 'allchecks.rst'),
                'wcag21mapping': str(temp_dir / 'misc' / 'wcag21-mapping.rst'),
                'priority_diff': str(temp_dir / 'misc' / 'priority-diff.rst'),
                'miscdefs': str(temp_dir / 'misc' / 'defs.txt'),
                'faq_index': str(temp_dir / 'faq' / 'index.rst'),
                'faq_article_index': str(temp_dir / 'faq' / 'articles' / 'index.rst'),
                'faq_tag_index': str(temp_dir / 'faq' / 'tags' / 'index.rst'),
                'makefile': str(temp_dir / 'incfiles.mk'),
                'axe_rules': str(temp_dir / 'misc' / 'axe-rules.rst')
            }
            mock_get_src.return_value = {'wcag_sc': str(temp_dir / 'wcag.json')}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            # Test with custom basedir
            with patch('sys.argv', ['yaml2rst', '--basedir', str(custom_basedir)]):
                yaml2rst.main()
            
            # Verify custom basedir was used
            mock_config.initialize.assert_called_once()
            config_call = mock_config.initialize.call_args[1]
            assert str(custom_basedir) in config_call['config_override']['basedir']

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('yaml2rst.yaml2rst.FileGenerator')
    @patch('os.makedirs')
    def test_cli_specific_files(
        self,
        mock_makedirs,
        mock_file_generator_class,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test CLI with specific files argument."""
        mock_file_generator = Mock()
        mock_file_generator_class.return_value = mock_file_generator
        
        # Create test files
        test_file1 = temp_dir / "test1.yaml"
        test_file2 = temp_dir / "test2.yaml"
        test_file1.touch()
        test_file2.touch()
        
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'guidelines': str(temp_dir),
                'checks': str(temp_dir / 'checks'),
                'faq_articles': str(temp_dir / 'faq'),
                'faq_tags': str(temp_dir / 'faq' / 'tags'),
                'info2gl': str(temp_dir / 'info'),
                'info2faq': str(temp_dir / 'info')
            }
            mock_get_static.return_value = {
                'all_checks': str(temp_dir / 'checks.rst'),
                'faq_index': str(temp_dir / 'faq' / 'index.rst'),
                'faq_tag_index': str(temp_dir / 'faq' / 'tags' / 'index.rst'),
                'faq_article_index': str(temp_dir / 'faq' / 'articles' / 'index.rst'),
                'wcag21mapping': str(temp_dir / 'info' / 'wcag21-mapping.rst'),
                'priority_diff': str(temp_dir / 'info' / 'priority.rst'),
                'miscdefs': str(temp_dir / 'inc' / 'miscdefs.txt'),
                'axe_rules': str(temp_dir / 'info' / 'axe-rules.rst'),
                'makefile': str(temp_dir / 'Makefile')
            }
            mock_get_src.return_value = {'wcag_sc': str(temp_dir / 'wcag.json')}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            # Test with specific files
            with patch('sys.argv', ['yaml2rst', str(test_file1), str(test_file2)]):
                yaml2rst.main()
            
            # Verify that generate was called with build_all=False and specific targets
            generate_calls = mock_file_generator.generate.call_args_list
            for call in generate_calls:
                config, build_all, targets = call[0]
                assert build_all is False
                assert str(test_file1) in targets
                assert str(test_file2) in targets

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_cli_help_message(self, mock_get_languages):
        """Test CLI help message."""
        mock_get_languages.return_value = ['ja', 'en']
        
        with patch('sys.argv', ['yaml2rst', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                initializer.parse_args()
            
            # Help should exit with code 0
            assert exc_info.value.code == 0

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_cli_invalid_language(self, mock_get_languages):
        """Test CLI with invalid language."""
        mock_get_languages.return_value = ['ja', 'en']
        
        with patch('sys.argv', ['yaml2rst', '--lang', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                initializer.parse_args()
            
            # Invalid argument should exit with non-zero code
            assert exc_info.value.code != 0

    def test_cli_argument_parsing_build_all(self):
        """Test argument parsing for build all mode."""
        with patch('sys.argv', ['yaml2rst', '--lang', 'ja', '--basedir', '/test']):
            args = initializer.parse_args()
            settings = initializer.process_arguments(args)
        
        assert settings['build_all'] is True
        assert settings['targets'] == []
        assert settings['lang'] == 'ja'

    def test_cli_argument_parsing_specific_files(self, temp_dir):
        """Test argument parsing for specific files mode."""
        # Create test files
        test_file1 = temp_dir / "test1.yaml"
        test_file2 = temp_dir / "test2.yaml"
        test_file1.touch()
        test_file2.touch()
        
        with patch('sys.argv', ['yaml2rst', str(test_file1), str(test_file2)]):
            args = initializer.parse_args()
            settings = initializer.process_arguments(args)
        
        assert settings['build_all'] is False
        assert len(settings['targets']) == 2
        assert str(test_file1) in settings['targets']
        assert str(test_file2) in settings['targets']

    @patch('yaml2rst.initializer.config.get_available_languages')
    def test_cli_short_arguments(self, mock_get_languages):
        """Test CLI with short argument forms."""
        mock_get_languages.return_value = ['ja', 'en']
        
        with patch('sys.argv', ['yaml2rst', '-l', 'en', '-b', '/custom/base']):
            args = initializer.parse_args()
        
        assert args.lang == 'en'
        assert args.basedir == '/custom/base'

    def test_cli_basedir_resolution(self, temp_dir):
        """Test that basedir is properly resolved to absolute path."""
        relative_path = "relative/path"
        
        with patch('sys.argv', ['yaml2rst', '--basedir', relative_path]):
            args = initializer.parse_args()
            settings = initializer.process_arguments(args)
        
        # Should be converted to absolute path
        assert os.path.isabs(settings['basedir'])
        assert relative_path in settings['basedir']

    def test_cli_file_path_resolution(self, temp_dir):
        """Test that file paths are properly resolved to absolute paths."""
        # Create test files with relative paths
        test_file = temp_dir / "test.yaml"
        test_file.touch()
        
        # Change to temp directory to test relative paths
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            with patch('sys.argv', ['yaml2rst', 'test.yaml']):
                args = initializer.parse_args()
                settings = initializer.process_arguments(args)
            
            # File paths should be converted to absolute
            assert len(settings['targets']) == 1
            assert os.path.isabs(settings['targets'][0])
            assert 'test.yaml' in settings['targets'][0]
            
        finally:
            os.chdir(original_cwd)


class TestCLIErrorHandling:
    """Test error handling in CLI interface."""

    @patch('yaml2rst.yaml2rst.Config')
    def test_cli_config_initialization_error(self, mock_config):
        """Test CLI behavior when Config initialization fails."""
        mock_config.initialize.side_effect = Exception("Config error")
        
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'guidelines': '/test/output/categories',
                'checks': '/test/output/checks',
                'faq_articles': '/test/output/faq',
                'faq_tags': '/test/output/faq/tags',
                'info2gl': '/test/output/info',
                'info2faq': '/test/output/info'
            }
            mock_get_static.return_value = {
                'all_checks': '/test/output/checks/checklist.rst',
                'faq_index': '/test/output/faq/index.rst',
                'faq_tag_index': '/test/output/faq/tags/index.rst',
                'faq_article_index': '/test/output/faq/articles/index.rst',
                'wcag21mapping': '/test/output/info/wcag21-mapping.rst',
                'priority_diff': '/test/output/info/priority.rst',
                'miscdefs': '/test/output/inc/miscdefs.txt',
                'axe_rules': '/test/output/info/axe-rules.rst',
                'makefile': '/test/output/Makefile'
            }
            mock_get_src.return_value = {'wcag_sc': '/test/wcag.json'}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            with patch('sys.argv', ['yaml2rst']):
                with pytest.raises(Exception, match="Config error"):
                    yaml2rst.main()

    @patch('os.makedirs')
    def test_cli_directory_creation_error(self, mock_makedirs):
        """Test CLI behavior when directory creation fails."""
        mock_makedirs.side_effect = OSError("Permission denied")
        
        with patch('yaml2rst.yaml2rst.Config') as mock_config, \
             patch('yaml2rst.yaml2rst.setup_instances') as mock_setup, \
             patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr:
            
            mock_get_dest.return_value = {
                'guidelines': '/test/dir',
                'checks': '/test/output/checks',
                'faq_articles': '/test/output/faq',
                'faq_tags': '/test/output/faq/tags',
                'info2gl': '/test/output/info',
                'info2faq': '/test/output/info'
            }
            mock_get_static.return_value = {
                'all_checks': '/test/output/checks/checklist.rst',
                'faq_index': '/test/output/faq/index.rst',
                'faq_tag_index': '/test/output/faq/tags/index.rst',
                'faq_article_index': '/test/output/faq/articles/index.rst',
                'wcag21mapping': '/test/output/info/wcag21-mapping.rst',
                'priority_diff': '/test/output/info/priority.rst',
                'miscdefs': '/test/output/inc/miscdefs.txt',
                'axe_rules': '/test/output/info/axe-rules.rst',
                'makefile': '/test/output/Makefile'
            }
            mock_get_src.return_value = {'wcag_sc': '/test/wcag.json'}
            
            mock_template = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            with patch('sys.argv', ['yaml2rst']):
                with pytest.raises(OSError, match="Permission denied"):
                    yaml2rst.main()

    def test_cli_nonexistent_files(self):
        """Test CLI behavior with nonexistent files."""
        nonexistent_file = "/path/to/nonexistent/file.yaml"
        
        with patch('sys.argv', ['yaml2rst', nonexistent_file]):
            args = initializer.parse_args()
            settings = initializer.process_arguments(args)
        
        # Should still process the arguments, even if files don't exist
        # The actual file existence check happens during generation
        assert settings['build_all'] is False
        assert nonexistent_file in settings['targets']


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    @patch('yaml2rst.yaml2rst.Config')
    @patch('yaml2rst.yaml2rst.setup_instances')
    @patch('freee_a11y_gl.Category.list_all')
    @patch('freee_a11y_gl.relationship_manager.RelationshipManager.get_sorted_related_objects')
    def test_cli_full_workflow(
        self,
        mock_get_related_objects,
        mock_list_all,
        mock_setup_instances,
        mock_config,
        temp_dir
    ):
        """Test complete CLI workflow with mocked dependencies."""
        # Setup mock data
        mock_category = Mock()
        mock_category.id = 'test_category'
        mock_category.title = 'Test Category'
        mock_category.description = 'Test'
        mock_category.get_dependency.return_value = ['/test/category.yaml']
        mock_list_all.return_value = [mock_category]
        
        mock_guideline = Mock()
        mock_guideline.template_data.return_value = {
            'id': 'test_gl', 'title': 'Test Guideline', 'priority': 'high'
        }
        mock_get_related_objects.return_value = [mock_guideline]
        
        # Setup output directories
        output_dir = temp_dir / "output"
        
        with patch('yaml2rst.initializer.get_dest_dirnames') as mock_get_dest, \
             patch('yaml2rst.initializer.get_static_dest_files') as mock_get_static, \
             patch('freee_a11y_gl.source.get_src_path') as mock_get_src, \
             patch('yaml2rst.initializer.TemplateManager') as mock_template_mgr, \
             patch('os.makedirs') as mock_makedirs:
            
            mock_get_dest.return_value = {
                'guidelines': str(output_dir / 'categories'),
                'checks': str(output_dir / 'checks'),
                'faq_articles': str(output_dir / 'faq'),
                'faq_tags': str(output_dir / 'faq' / 'tags'),
                'info2gl': str(output_dir / 'info'),
                'info2faq': str(output_dir / 'info')
            }
            mock_get_static.return_value = {
                'all_checks': str(output_dir / 'checks.rst'),
                'faq_index': str(output_dir / 'faq' / 'index.rst'),
                'faq_tag_index': str(output_dir / 'faq' / 'tags' / 'index.rst'),
                'faq_article_index': str(output_dir / 'faq' / 'articles' / 'index.rst'),
                'wcag21mapping': str(output_dir / 'info' / 'wcag21-mapping.rst'),
                'priority_diff': str(output_dir / 'info' / 'priority.rst'),
                'miscdefs': str(output_dir / 'inc' / 'miscdefs.txt'),
                'axe_rules': str(output_dir / 'info' / 'axe-rules.rst'),
                'makefile': str(output_dir / 'Makefile')
            }
            mock_get_src.return_value = {'wcag_sc': str(temp_dir / 'wcag.json')}
            
            # Setup template mock
            mock_template = Mock()
            mock_template.write_rst = Mock()
            mock_template_manager = Mock()
            mock_template_manager.load.return_value = mock_template
            mock_template_mgr.return_value = mock_template_manager
            
            # Execute CLI
            with patch('sys.argv', ['yaml2rst', '--basedir', str(temp_dir), '--lang', 'ja']):
                yaml2rst.main()
            
            # Verify the workflow completed
            mock_config.initialize.assert_called_once()
            mock_setup_instances.assert_called_once()
            
            # Verify files would have been generated
            assert mock_template.write_rst.call_count > 0

    def test_cli_argument_validation(self):
        """Test CLI argument validation."""
        # Test that all required components are properly validated
        with patch('yaml2rst.initializer.config.get_available_languages') as mock_langs:
            mock_langs.return_value = ['ja', 'en']
            
            # Valid arguments should parse successfully
            with patch('sys.argv', ['yaml2rst', '--lang', 'ja', '--basedir', '/test']):
                args = initializer.parse_args()
                assert args.lang == 'ja'
                assert args.basedir == '/test'
            
            # Invalid language should fail
            with patch('sys.argv', ['yaml2rst', '--lang', 'invalid']):
                with pytest.raises(SystemExit):
                    initializer.parse_args()
