"""
Tests for config_loader module.

Tests the simplified implementation of configuration loading including:
- YAML format support only
- Configuration file search logic
- Path resolution
- Pydantic validation
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
import yaml

from yaml2sheet.config_loader import (
    ApplicationConfig,
    YAMLConfigLoader,
    find_config_file,
    load_configuration,
    create_default_config,
    validate_readable_file
)


class TestApplicationConfig:
    """Test ApplicationConfig model validation and methods."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = ApplicationConfig()
        assert config.credentials_path == Path("credentials.json")
        assert config.token_path == Path("token.json")
        assert config.development_spreadsheet_id == ""
        assert config.production_spreadsheet_id == ""
        assert config.sheet_editor_email == ""
        assert config.log_level == "INFO"
        assert config.basedir is None
        assert config.base_url == "https://a11y-guidelines.freee.co.jp"
        assert config.version_info_cell == "A27"
    
    
    def test_get_log_level(self):
        """Test log level conversion to logging constants."""
        import logging
        
        config = ApplicationConfig(log_level="DEBUG")
        assert config.get_log_level() == logging.DEBUG
        
        config = ApplicationConfig(log_level="INFO")
        assert config.get_log_level() == logging.INFO
        
        config = ApplicationConfig(log_level="WARNING")
        assert config.get_log_level() == logging.WARNING
        
        config = ApplicationConfig(log_level="ERROR")
        assert config.get_log_level() == logging.ERROR
        
        config = ApplicationConfig(log_level="CRITICAL")
        assert config.get_log_level() == logging.CRITICAL
    
    def test_get_spreadsheet_id_development(self):
        """Test getting development spreadsheet ID."""
        config = ApplicationConfig(development_spreadsheet_id="dev_id")
        assert config.get_spreadsheet_id(production=False) == "dev_id"
    
    def test_get_spreadsheet_id_production(self):
        """Test getting production spreadsheet ID."""
        config = ApplicationConfig(production_spreadsheet_id="prod_id")
        assert config.get_spreadsheet_id(production=True) == "prod_id"
    
    def test_get_spreadsheet_id_missing_development(self):
        """Test error when development spreadsheet ID is missing."""
        config = ApplicationConfig()
        with pytest.raises(ValueError, match="Development spreadsheet ID is not set"):
            config.get_spreadsheet_id(production=False)
    
    def test_get_spreadsheet_id_missing_production(self):
        """Test error when production spreadsheet ID is missing."""
        config = ApplicationConfig()
        with pytest.raises(ValueError, match="Production spreadsheet ID is not set"):
            config.get_spreadsheet_id(production=True)
    
    def test_get_base_url_default(self):
        """Test getting default base URL."""
        config = ApplicationConfig()
        assert config.get_base_url() == "https://a11y-guidelines.freee.co.jp"
    
    def test_get_base_url_command_line_override(self):
        """Test command line base URL override."""
        config = ApplicationConfig(base_url="https://config.example.com")
        assert config.get_base_url("https://cmd.example.com") == "https://cmd.example.com"
    
    def test_get_basedir_default(self, temp_dir):
        """Test getting default base directory."""
        config = ApplicationConfig()
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            result = config.get_basedir()
            assert result == temp_dir.resolve()
    
    def test_get_basedir_from_config(self, temp_dir):
        """Test getting base directory from config."""
        config = ApplicationConfig(basedir=temp_dir)
        result = config.get_basedir()
        assert result == temp_dir.resolve()
    
    def test_get_basedir_command_line_override(self, temp_dir):
        """Test command line base directory override."""
        config_dir = temp_dir / "config"
        config_dir.mkdir()
        cmd_dir = temp_dir / "cmd"
        cmd_dir.mkdir()
        
        config = ApplicationConfig(basedir=config_dir)
        result = config.get_basedir(cmd_dir)
        assert result == cmd_dir.resolve()
    
    def test_get_basedir_nonexistent_directory(self):
        """Test error when base directory doesn't exist."""
        config = ApplicationConfig()
        with pytest.raises(ValueError, match="Base directory does not exist"):
            config.get_basedir("/nonexistent/directory")
    
    def test_resolve_credential_paths_relative(self, temp_dir):
        """Test resolving relative credential paths."""
        config_file = temp_dir / "config.yaml"
        config_file.touch()
        
        config_data = {
            "credentials_path": "relative/creds.json",
            "token_path": "relative/token.json"
        }
        
        context = {"config_file_path": config_file}
        config = ApplicationConfig.model_validate(config_data, context=context)
        
        expected_creds = temp_dir / "relative/creds.json"
        expected_token = temp_dir / "relative/token.json"
        
        assert config.credentials_path == expected_creds
        assert config.token_path == expected_token
    
    def test_resolve_credential_paths_absolute(self, temp_dir):
        """Test that absolute credential paths are not modified."""
        config_file = temp_dir / "config.yaml"
        config_file.touch()
        
        abs_creds = temp_dir / "abs_creds.json"
        abs_token = temp_dir / "abs_token.json"
        
        config_data = {
            "credentials_path": str(abs_creds),
            "token_path": str(abs_token)
        }
        
        context = {"config_file_path": config_file}
        config = ApplicationConfig.model_validate(config_data, context=context)
        
        assert config.credentials_path == abs_creds
        assert config.token_path == abs_token

    def test_version_info_cell_validation_valid(self):
        """Test valid version_info_cell formats."""
        valid_cells = ["A27", "B15", "Z100", "AA1", "AB123"]
        for cell in valid_cells:
            config = ApplicationConfig(version_info_cell=cell)
            assert config.version_info_cell == cell.upper()

    def test_version_info_cell_validation_invalid(self):
        """Test invalid version_info_cell formats."""
        invalid_cells = ["A", "27", "A27B", "1A", "A-27", ""]
        for cell in invalid_cells:
            with pytest.raises(ValueError, match="version_info_cell must be in Excel format"):
                ApplicationConfig(version_info_cell=cell)

    def test_parse_version_info_cell_simple(self):
        """Test parsing simple cell references."""
        config = ApplicationConfig(version_info_cell="A27")
        row_index, column_index = config.parse_version_info_cell()
        assert row_index == 26  # 0-based
        assert column_index == 0  # A = 0

        config = ApplicationConfig(version_info_cell="B15")
        row_index, column_index = config.parse_version_info_cell()
        assert row_index == 14  # 0-based
        assert column_index == 1  # B = 1

    def test_parse_version_info_cell_multi_column(self):
        """Test parsing multi-column cell references."""
        config = ApplicationConfig(version_info_cell="AA1")
        row_index, column_index = config.parse_version_info_cell()
        assert row_index == 0  # 0-based
        assert column_index == 26  # AA = 26

        config = ApplicationConfig(version_info_cell="AB10")
        row_index, column_index = config.parse_version_info_cell()
        assert row_index == 9  # 0-based
        assert column_index == 27  # AB = 27

    def test_parse_version_info_cell_case_insensitive(self):
        """Test that cell parsing is case insensitive."""
        config = ApplicationConfig(version_info_cell="a27")
        row_index, column_index = config.parse_version_info_cell()
        assert row_index == 26
        assert column_index == 0
        assert config.version_info_cell == "A27"  # Should be normalized to uppercase


class TestConfigLoaders:
    """Test configuration file loaders."""
    
    def test_yaml_config_loader_load(self, sample_yaml_config_file):
        """Test YAML configuration loading."""
        loader = YAMLConfigLoader()
        data = loader.load(sample_yaml_config_file)
        
        assert data["credentials_path"] == "credentials.json"
        assert data["development_spreadsheet_id"] == "test_dev_spreadsheet_id"
    
    def test_yaml_config_loader_save(self, temp_dir):
        """Test YAML configuration saving."""
        loader = YAMLConfigLoader()
        config_data = {"test_key": "test_value"}
        config_file = temp_dir / "test_save.yaml"
        
        loader.save(config_data, config_file)
        
        assert config_file.exists()
        with open(config_file) as f:
            loaded_data = yaml.safe_load(f)
        assert loaded_data == config_data
    
    def test_yaml_config_loader_invalid_yaml(self, temp_dir):
        """Test YAML loader with invalid YAML."""
        loader = YAMLConfigLoader()
        invalid_yaml_file = temp_dir / "invalid.yaml"
        with open(invalid_yaml_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        with pytest.raises(ValueError, match="Invalid YAML in config file"):
            loader.load(invalid_yaml_file)


class TestFindConfigFile:
    """Test configuration file finding logic."""
    
    def test_find_config_file_absolute_path_exists(self, sample_yaml_config_file):
        """Test finding config file with absolute path that exists."""
        result = find_config_file(sample_yaml_config_file)
        assert result == sample_yaml_config_file
    
    def test_find_config_file_absolute_path_not_exists(self, temp_dir):
        """Test error when absolute path doesn't exist."""
        nonexistent_file = temp_dir / "nonexistent.yaml"
        with pytest.raises(FileNotFoundError, match="Specified configuration file not found"):
            find_config_file(nonexistent_file)
    
    def test_find_config_file_relative_path_exists(self, temp_dir):
        """Test finding config file with relative path in current directory."""
        config_file = temp_dir / "config.yaml"
        config_file.touch()
        
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            result = find_config_file("config.yaml")
            assert result == config_file
    
    def test_find_config_file_relative_path_not_exists(self, temp_dir):
        """Test error when relative path doesn't exist in current directory."""
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            with pytest.raises(FileNotFoundError, match="Specified configuration file not found"):
                find_config_file("nonexistent.yaml")
    
    def test_find_config_file_default_search_home_config(self, temp_dir):
        """Test default search in home config directory."""
        home_config_dir = temp_dir / ".config" / "freee_a11y_gl"
        home_config_dir.mkdir(parents=True)
        config_file = home_config_dir / "yaml2sheet.yaml"
        config_file.touch()
        
        with patch('pathlib.Path.home', return_value=temp_dir), \
             patch('pathlib.Path.cwd', return_value=temp_dir / "other"):
            result = find_config_file()
            assert result == config_file
    
    def test_find_config_file_default_search_current_dir(self, temp_dir):
        """Test default search in current directory."""
        config_file = temp_dir / ".yaml2sheet.yaml"
        config_file.touch()
        
        with patch('pathlib.Path.home', return_value=temp_dir / "home"), \
             patch('pathlib.Path.cwd', return_value=temp_dir):
            result = find_config_file()
            assert result == config_file
    
    def test_find_config_file_default_search_priority(self, temp_dir):
        """Test that home config directory has priority over current directory."""
        # Create config in both locations
        home_config_dir = temp_dir / ".config" / "freee_a11y_gl"
        home_config_dir.mkdir(parents=True)
        home_config_file = home_config_dir / "yaml2sheet.yaml"
        home_config_file.touch()
        
        current_config_file = temp_dir / ".yaml2sheet.yaml"
        current_config_file.touch()
        
        with patch('pathlib.Path.home', return_value=temp_dir), \
             patch('pathlib.Path.cwd', return_value=temp_dir):
            result = find_config_file()
            assert result == home_config_file  # Home config should have priority
    
    def test_find_config_file_extension_priority(self, temp_dir):
        """Test file extension priority in default search."""
        config_dir = temp_dir / ".config" / "freee_a11y_gl"
        config_dir.mkdir(parents=True)
        
        # Create files with different YAML extensions
        yaml_file = config_dir / "yaml2sheet.yaml"
        yml_file = config_dir / "yaml2sheet.yml"
        
        # Create in reverse priority order
        yml_file.touch()
        yaml_file.touch()
        
        with patch('pathlib.Path.home', return_value=temp_dir), \
             patch('pathlib.Path.cwd', return_value=temp_dir / "other"):
            result = find_config_file()
            assert result == yaml_file  # .yaml should have highest priority
    
    def test_find_config_file_not_found(self, temp_dir):
        """Test error when no config file is found."""
        with patch('pathlib.Path.home', return_value=temp_dir), \
             patch('pathlib.Path.cwd', return_value=temp_dir):
            with pytest.raises(FileNotFoundError, match="No YAML configuration file found"):
                find_config_file()


class TestLoadConfiguration:
    """Test configuration loading integration."""
    
    def test_load_configuration_yaml(self, sample_yaml_config_file):
        """Test loading YAML configuration."""
        config = load_configuration(sample_yaml_config_file)
        assert isinstance(config, ApplicationConfig)
        assert config.development_spreadsheet_id == "test_dev_spreadsheet_id"
    
    
    def test_load_configuration_file_not_found(self, temp_dir):
        """Test error when configuration file is not found."""
        with patch('pathlib.Path.cwd', return_value=temp_dir), \
             patch('pathlib.Path.home', return_value=temp_dir):
            with pytest.raises(FileNotFoundError):
                load_configuration()
    
    def test_load_configuration_validation_error(self, temp_dir):
        """Test error when configuration validation fails."""
        invalid_config_file = temp_dir / "invalid.yaml"
        with open(invalid_config_file, 'w') as f:
            yaml.dump({"log_level": "INVALID_LEVEL"}, f)
        
        with pytest.raises(ValueError, match="Invalid configuration"):
            load_configuration(invalid_config_file)


class TestCreateDefaultConfig:
    """Test default configuration creation."""
    
    def test_create_default_config_yaml(self, temp_dir):
        """Test creating default YAML configuration."""
        output_path = temp_dir / "default.yaml"
        result_path = create_default_config(output_path)
        
        assert result_path == output_path
        assert output_path.exists()
        
        with open(output_path) as f:
            data = yaml.safe_load(f)
        
        assert data["credentials_path"] == "credentials.json"
        assert data["token_path"] == "token.json"
        assert data["log_level"] == "INFO"
        assert data["base_url"] == "https://a11y-guidelines.freee.co.jp"
        assert data["version_info_cell"] == "A27"
    
    
    def test_create_default_config_default_path(self, temp_dir):
        """Test creating default configuration with default path."""
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            result_path = create_default_config()
            expected_path = temp_dir / "yaml2sheet.yaml"
            
            assert result_path == expected_path
            assert expected_path.exists()
    
    def test_create_default_config_create_directories(self, temp_dir):
        """Test that directories are created if they don't exist."""
        nested_path = temp_dir / "nested" / "dir" / "config.yaml"
        result_path = create_default_config(nested_path)
        
        assert result_path == nested_path
        assert nested_path.exists()
        assert nested_path.parent.exists()


class TestValidateReadableFile:
    """Test file validation utility."""
    
    def test_validate_readable_file_exists(self, temp_dir):
        """Test validating existing readable file."""
        test_file = temp_dir / "test.txt"
        test_file.touch()
        
        result = validate_readable_file(test_file)
        assert result == test_file
    
    def test_validate_readable_file_not_exists(self, temp_dir):
        """Test error when file doesn't exist."""
        nonexistent_file = temp_dir / "nonexistent.txt"
        
        with pytest.raises(ValueError, match="File does not exist"):
            validate_readable_file(nonexistent_file)
    
    def test_validate_readable_file_string_path(self, temp_dir):
        """Test validating file with string path."""
        test_file = temp_dir / "test.txt"
        test_file.touch()
        
        result = validate_readable_file(str(test_file))
        assert result == test_file
    
    @pytest.mark.skipif(os.name == 'nt', reason="Permission tests don't work reliably on Windows")
    def test_validate_readable_file_not_readable(self, temp_dir):
        """Test error when file is not readable."""
        test_file = temp_dir / "test.txt"
        test_file.touch()
        test_file.chmod(0o000)  # Remove all permissions
        
        try:
            with pytest.raises(ValueError, match="File is not readable"):
                validate_readable_file(test_file)
        finally:
            test_file.chmod(0o644)  # Restore permissions for cleanup
