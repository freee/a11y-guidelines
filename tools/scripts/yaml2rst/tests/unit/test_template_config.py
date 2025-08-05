"""Tests for template configuration management."""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from yaml2rst.template_config import TemplateConfig, TemplateConfigError


class TestTemplateConfig:
    """Test cases for TemplateConfig class."""

    def test_default_values(self):
        """Test that default configuration values are correct."""
        config = TemplateConfig()

        # Test default constants
        assert config.DEFAULT_USER_DIR == "~/.config/freee_a11y_gl/templates"
        default_config = "~/.config/freee_a11y_gl/yaml2rst.conf"
        assert config.DEFAULT_CONFIG_FILE == default_config
        assert config.DEFAULT_FALLBACK_TO_BUILTIN is True

        # Test environment variable names
        assert config.ENV_USER_TEMPLATE_DIR == "YAML2RST_USER_TEMPLATE_DIR"
        assert config.ENV_CONFIG_FILE == "YAML2RST_CONFIG_FILE"
        fallback_env = "YAML2RST_FALLBACK_TO_BUILTIN"
        assert config.ENV_FALLBACK_TO_BUILTIN == fallback_env

    def test_init_with_custom_config_file(self):
        """Test initialization with custom config file path."""
        custom_path = "/custom/config.conf"
        config = TemplateConfig(config_file=custom_path)

        assert config._config_file == custom_path
        assert config._config_cache is None

    def test_get_config_file_path_custom(self):
        """Test getting config file path with custom file."""
        custom_path = "/custom/config.conf"
        config = TemplateConfig(config_file=custom_path)

        result = config.get_config_file_path()
        assert result == Path(custom_path).expanduser()

    @patch.dict(os.environ, {'YAML2RST_CONFIG_FILE': '/env/config.conf'})
    def test_get_config_file_path_env_var(self):
        """Test getting config file path from environment variable."""
        config = TemplateConfig()

        result = config.get_config_file_path()
        assert result == Path('/env/config.conf').expanduser()

    @patch.dict(os.environ, {}, clear=True)
    def test_get_config_file_path_default(self):
        """Test getting config file path with default value."""
        config = TemplateConfig()

        result = config.get_config_file_path()
        expected = Path("~/.config/freee_a11y_gl/yaml2rst.conf").expanduser()
        assert result == expected

    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_defaults_only(self):
        """Test loading config with only default values."""
        config = TemplateConfig()

        with patch.object(config, 'get_config_file_path') as mock_path:
            mock_path.return_value = Path('/nonexistent/config.conf')

            result = config.load_config()

            expected = {
                'user_template_dir': "~/.config/freee_a11y_gl/templates",
                'fallback_to_builtin': True
            }
            assert result == expected

    def test_load_config_caching(self):
        """Test that configuration is cached after first load."""
        config = TemplateConfig()

        with patch.object(config, 'get_config_file_path') as mock_path:
            mock_path.return_value = Path('/nonexistent/config.conf')

            # First call
            result1 = config.load_config()
            # Second call should return cached result
            result2 = config.load_config()

            assert result1 is result2
            # get_config_file_path should only be called once due to caching
            assert mock_path.call_count == 1

    def test_clear_cache(self):
        """Test clearing configuration cache."""
        config = TemplateConfig()

        with patch.object(config, 'get_config_file_path') as mock_path:
            mock_path.return_value = Path('/nonexistent/config.conf')

            # Load config to populate cache
            config.load_config()
            assert config._config_cache is not None

            # Clear cache
            config.clear_cache()
            assert config._config_cache is None

    def test_load_config_file_valid(self):
        """Test loading valid configuration file."""
        config_content = """
[templates]
user_template_dir = /custom/templates
fallback_to_builtin = false
"""
        config = TemplateConfig()
        config_path = Path('/test/config.conf')

        with patch('builtins.open', mock_open(read_data=config_content)):
            result = config._load_config_file(config_path)

            expected = {
                'user_template_dir': '/custom/templates',
                'fallback_to_builtin': False
            }
            assert result == expected

    def test_load_config_file_partial(self):
        """Test loading configuration file with only some values."""
        config_content = """
[templates]
user_template_dir = /custom/templates
"""
        config = TemplateConfig()
        config_path = Path('/test/config.conf')

        with patch('builtins.open', mock_open(read_data=config_content)):
            result = config._load_config_file(config_path)

            expected = {
                'user_template_dir': '/custom/templates'
            }
            assert result == expected

    def test_load_config_file_no_templates_section(self):
        """Test loading configuration file without templates section."""
        config_content = """
[other]
some_value = test
"""
        config = TemplateConfig()
        config_path = Path('/test/config.conf')

        with patch('builtins.open', mock_open(read_data=config_content)):
            result = config._load_config_file(config_path)

            assert result == {}

    def test_load_config_file_invalid_boolean(self):
        """Test loading configuration file with invalid boolean value."""
        config_content = """
[templates]
fallback_to_builtin = invalid_value
"""
        config = TemplateConfig()
        config_path = Path('/test/config.conf')

        with patch('builtins.open', mock_open(read_data=config_content)):
            error_match = "Invalid boolean value"
            with pytest.raises(TemplateConfigError, match=error_match):
                config._load_config_file(config_path)

    def test_load_config_file_invalid_format(self):
        """Test loading malformed configuration file."""
        config_content = "invalid config format"
        config = TemplateConfig()
        config_path = Path('/test/config.conf')

        with patch('builtins.open', mock_open(read_data=config_content)):
            error_match = "Invalid configuration file format"
            with pytest.raises(TemplateConfigError, match=error_match):
                config._load_config_file(config_path)

    @patch.dict(os.environ, {}, clear=True)
    def test_load_env_overrides_empty(self):
        """Test loading environment overrides when none are set."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        assert result == {}

    @patch.dict(os.environ, {
        'YAML2RST_USER_TEMPLATE_DIR': '/env/templates'
    })
    def test_load_env_overrides_string_value(self):
        """Test loading string environment override."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'user_template_dir': '/env/templates'
        }
        assert result == expected

    @patch.dict(os.environ, {
        'YAML2RST_FALLBACK_TO_BUILTIN': 'true'
    })
    def test_load_env_overrides_boolean_true(self):
        """Test loading boolean environment override (true)."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'fallback_to_builtin': True
        }
        assert result == expected

    @patch.dict(os.environ, {
        'YAML2RST_FALLBACK_TO_BUILTIN': 'false'
    })
    def test_load_env_overrides_boolean_false(self):
        """Test loading boolean environment override (false)."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'fallback_to_builtin': False
        }
        assert result == expected

    @patch.dict(os.environ, {
        'YAML2RST_FALLBACK_TO_BUILTIN': '1'
    })
    def test_load_env_overrides_boolean_numeric_true(self):
        """Test loading boolean environment override (numeric true)."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'fallback_to_builtin': True
        }
        assert result == expected

    @patch.dict(os.environ, {
        'YAML2RST_FALLBACK_TO_BUILTIN': '0'
    })
    def test_load_env_overrides_boolean_numeric_false(self):
        """Test loading boolean environment override (numeric false)."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'fallback_to_builtin': False
        }
        assert result == expected

    @patch.dict(os.environ, {
        'YAML2RST_FALLBACK_TO_BUILTIN': 'invalid'
    })
    def test_load_env_overrides_boolean_invalid(self, caplog):
        """Test loading invalid boolean environment override."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        assert result == {}

        # Check that warning was logged
        assert "Invalid boolean value" in caplog.text

    @patch.dict(os.environ, {
        'YAML2RST_USER_TEMPLATE_DIR': '/env/templates',
        'YAML2RST_FALLBACK_TO_BUILTIN': 'false'
    })
    def test_load_env_overrides_multiple(self):
        """Test loading multiple environment overrides."""
        config = TemplateConfig()

        result = config._load_env_overrides()
        expected = {
            'user_template_dir': '/env/templates',
            'fallback_to_builtin': False
        }
        assert result == expected

    def test_get_user_template_dir(self):
        """Test getting user template directory."""
        config = TemplateConfig()

        with patch.object(config, 'load_config') as mock_load:
            mock_load.return_value = {
                'user_template_dir': '/test/templates',
                'fallback_to_builtin': True
            }

            result = config.get_user_template_dir()
            assert result == '/test/templates'

    def test_get_user_template_dir_expanded(self):
        """Test getting expanded user template directory path."""
        config = TemplateConfig()

        with patch.object(config, 'get_user_template_dir') as mock_get:
            mock_get.return_value = '~/test/templates'

            result = config.get_user_template_dir_expanded()
            expected = Path('~/test/templates').expanduser()
            assert result == expected

    def test_should_fallback_to_builtin_true(self):
        """Test fallback to builtin when enabled."""
        config = TemplateConfig()

        with patch.object(config, 'load_config') as mock_load:
            mock_load.return_value = {
                'user_template_dir': '/test/templates',
                'fallback_to_builtin': True
            }

            result = config.should_fallback_to_builtin()
            assert result is True

    def test_should_fallback_to_builtin_false(self):
        """Test fallback to builtin when disabled."""
        config = TemplateConfig()

        with patch.object(config, 'load_config') as mock_load:
            mock_load.return_value = {
                'user_template_dir': '/test/templates',
                'fallback_to_builtin': False
            }

            result = config.should_fallback_to_builtin()
            assert result is False

    def test_get_template_search_paths_custom_only(self):
        """Test getting search paths with custom directory only."""
        config = TemplateConfig()

        mock_user_dir_name = 'get_user_template_dir_expanded'
        mock_fallback_name = 'should_fallback_to_builtin'
        with patch.object(config, mock_user_dir_name) as mock_user_dir:
            with patch.object(config, mock_fallback_name) as mock_fallback:
                user_path = Path('/nonexistent/user/templates')
                mock_user_dir.return_value = user_path
                mock_fallback.return_value = True

                custom_dir = '/custom/templates'
                result = config.get_template_search_paths(
                    custom_dir=custom_dir)

                # Should include custom dir and builtin (user dir doesn't
                # exist)
                assert '/custom/templates' in result
                # builtin path
                assert any('templates' in path for path in result)

    def test_get_template_search_paths_all_sources(self, tmp_path):
        """Test getting search paths with all sources available."""
        config = TemplateConfig()

        # Create a temporary user directory
        user_dir = tmp_path / "user_templates"
        user_dir.mkdir()

        mock_user_dir_name = 'get_user_template_dir_expanded'
        mock_fallback_name = 'should_fallback_to_builtin'
        with patch.object(config, mock_user_dir_name) as mock_user_dir:
            with patch.object(config, mock_fallback_name) as mock_fallback:
                mock_user_dir.return_value = user_dir
                mock_fallback.return_value = True

                custom_dir = '/custom/templates'
                result = config.get_template_search_paths(
                    custom_dir=custom_dir)

                # Should include all three sources
                assert '/custom/templates' in result
                assert str(user_dir) in result
                # builtin path
                assert any('templates' in path for path in result)

                # Custom should be first, user second, builtin last
                assert result[0] == '/custom/templates'
                assert result[1] == str(user_dir)

    def test_get_template_search_paths_no_fallback(self, tmp_path):
        """Test getting search paths with fallback disabled."""
        config = TemplateConfig()

        user_dir = tmp_path / "user_templates"
        user_dir.mkdir()

        mock_user_dir_name = 'get_user_template_dir_expanded'
        mock_fallback_name = 'should_fallback_to_builtin'
        with patch.object(config, mock_user_dir_name) as mock_user_dir:
            with patch.object(config, mock_fallback_name) as mock_fallback:
                mock_user_dir.return_value = user_dir
                mock_fallback.return_value = False

                result = config.get_template_search_paths()

                # Should only include user directory
                assert result == [str(user_dir)]

    def test_validate_config_valid(self, tmp_path):
        """Test configuration validation with valid setup."""
        config = TemplateConfig()

        user_dir = tmp_path / "templates"
        user_dir.mkdir()

        with patch.object(config, 'load_config') as mock_load:
            mock_paths_name = 'get_template_search_paths'
            with patch.object(config, mock_paths_name) as mock_paths:
                mock_load.return_value = {
                    'user_template_dir': str(user_dir),
                    'fallback_to_builtin': True
                }
                mock_paths.return_value = [str(user_dir)]

                warnings = config.validate_config()
                assert warnings == []

    def test_validate_config_user_dir_not_directory(self, tmp_path):
        """Test configuration validation when user dir is not a directory."""
        config = TemplateConfig()

        # Create a file instead of directory
        user_file = tmp_path / "templates"
        user_file.write_text("not a directory")

        with patch.object(config, 'load_config') as mock_load:
            mock_paths_name = 'get_template_search_paths'
            with patch.object(config, mock_paths_name) as mock_paths:
                mock_load.return_value = {
                    'user_template_dir': str(user_file),
                    'fallback_to_builtin': True
                }
                mock_paths.return_value = [str(user_file)]

                warnings = config.validate_config()
                assert len(warnings) == 1
                assert "not a directory" in warnings[0]

    def test_validate_config_no_valid_paths(self):
        """Test configuration validation with no valid template paths."""
        config = TemplateConfig()

        with patch.object(config, 'load_config') as mock_load:
            mock_paths_name = 'get_template_search_paths'
            with patch.object(config, mock_paths_name) as mock_paths:
                mock_load.return_value = {
                    'user_template_dir': '/nonexistent',
                    'fallback_to_builtin': True
                }
                paths = ['/nonexistent/path1', '/nonexistent/path2']
                mock_paths.return_value = paths

                warnings = config.validate_config()
                assert len(warnings) == 1
                assert "No valid template directories found" in warnings[0]

    def test_integration_config_file_and_env_override(self, tmp_path):
        """Test integration of config file loading with env overrides."""
        config_file = tmp_path / "config.conf"
        config_file.write_text("""
[templates]
user_template_dir = /config/templates
fallback_to_builtin = true
""")

        config = TemplateConfig(config_file=str(config_file))

        with patch.dict(os.environ, {
            'YAML2RST_USER_TEMPLATE_DIR': '/env/templates',
            'YAML2RST_FALLBACK_TO_BUILTIN': 'false'
        }):
            result = config.load_config()

            # Environment variables should override config file
            expected = {
                'user_template_dir': '/env/templates',
                'fallback_to_builtin': False
            }
            assert result == expected

    def test_integration_full_workflow(self, tmp_path):
        """Test complete workflow from config loading to path resolution."""
        # Set up directories
        user_dir = tmp_path / "user_templates"
        user_dir.mkdir()
        custom_dir = tmp_path / "custom_templates"
        custom_dir.mkdir()

        # Create config file
        config_file = tmp_path / "config.conf"
        config_file.write_text(f"""
[templates]
user_template_dir = {user_dir}
fallback_to_builtin = true
""")

        config = TemplateConfig(config_file=str(config_file))

        # Test the complete workflow
        loaded_config = config.load_config()
        assert loaded_config['user_template_dir'] == str(user_dir)

        user_dir_path = config.get_user_template_dir_expanded()
        assert user_dir_path == user_dir

        search_paths = config.get_template_search_paths(
            custom_dir=str(custom_dir))
        assert str(custom_dir) in search_paths
        assert str(user_dir) in search_paths

        warnings = config.validate_config()
        assert warnings == []  # Should be valid
