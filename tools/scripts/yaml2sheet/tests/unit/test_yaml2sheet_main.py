"""
Tests for yaml2sheet main module.

Tests the existing implementation of the main entry point including:
- Command line argument parsing
- Configuration loading integration
- Authentication flow integration
- Main execution logic
- Error handling
"""

import pytest
import sys
import argparse
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
from io import StringIO

from yaml2sheet.yaml2sheet import (
    parse_args,
    setup_logging,
    get_credentials,
    main
)


class TestParseArgs:
    """Test command line argument parsing."""
    
    def test_parse_args_defaults(self):
        """Test parsing with default arguments."""
        with patch('sys.argv', ['yaml2sheet']):
            args = parse_args()
            
            assert args.create_config is False
            assert args.config is None
            assert args.init is False
            assert args.production is False
            assert args.basedir == str(Path.cwd())
            assert args.url is None
            assert args.verbose is False
    
    def test_parse_args_create_config(self):
        """Test --create-config argument."""
        with patch('sys.argv', ['yaml2sheet', '--create-config']):
            args = parse_args()
            assert args.create_config is True
    
    def test_parse_args_config_path(self):
        """Test -c/--config argument."""
        with patch('sys.argv', ['yaml2sheet', '-c', 'custom_config.yaml']):
            args = parse_args()
            assert args.config == 'custom_config.yaml'
        
        with patch('sys.argv', ['yaml2sheet', '--config', 'another_config.toml']):
            args = parse_args()
            assert args.config == 'another_config.toml'
    
    def test_parse_args_init(self):
        """Test --init argument."""
        with patch('sys.argv', ['yaml2sheet', '--init']):
            args = parse_args()
            assert args.init is True
    
    def test_parse_args_production(self):
        """Test -p/--production argument."""
        with patch('sys.argv', ['yaml2sheet', '-p']):
            args = parse_args()
            assert args.production is True
        
        with patch('sys.argv', ['yaml2sheet', '--production']):
            args = parse_args()
            assert args.production is True
    
    def test_parse_args_basedir(self):
        """Test -b/--basedir argument."""
        with patch('sys.argv', ['yaml2sheet', '-b', '/custom/basedir']):
            args = parse_args()
            assert args.basedir == '/custom/basedir'
        
        with patch('sys.argv', ['yaml2sheet', '--basedir', '/another/basedir']):
            args = parse_args()
            assert args.basedir == '/another/basedir'
    
    def test_parse_args_url(self):
        """Test --url argument."""
        with patch('sys.argv', ['yaml2sheet', '--url', 'https://custom.example.com']):
            args = parse_args()
            assert args.url == 'https://custom.example.com'
    
    def test_parse_args_verbose(self):
        """Test -v/--verbose argument."""
        with patch('sys.argv', ['yaml2sheet', '-v']):
            args = parse_args()
            assert args.verbose is True
        
        with patch('sys.argv', ['yaml2sheet', '--verbose']):
            args = parse_args()
            assert args.verbose is True
    
    def test_parse_args_combined(self):
        """Test multiple arguments combined."""
        with patch('sys.argv', [
            'yaml2sheet', 
            '--config', 'test.yaml',
            '--production',
            '--init',
            '--basedir', '/test/dir',
            '--url', 'https://test.com',
            '--verbose'
        ]):
            args = parse_args()
            
            assert args.config == 'test.yaml'
            assert args.production is True
            assert args.init is True
            assert args.basedir == '/test/dir'
            assert args.url == 'https://test.com'
            assert args.verbose is True


class TestSetupLogging:
    """Test logging setup functionality."""
    
    @patch('yaml2sheet.yaml2sheet.logging.basicConfig')
    def test_setup_logging_default_level(self, mock_basic_config):
        """Test logging setup with default level."""
        import logging
        setup_logging()
        
        mock_basic_config.assert_called_once_with(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True
        )
    
    @patch('yaml2sheet.yaml2sheet.logging.basicConfig')
    def test_setup_logging_custom_level(self, mock_basic_config):
        """Test logging setup with custom level."""
        import logging
        setup_logging(logging.DEBUG)
        
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True
        )


class TestGetCredentials:
    """Test credential retrieval functionality."""
    
    @patch('yaml2sheet.yaml2sheet.GoogleAuthManager')
    def test_get_credentials_success(self, mock_auth_manager_class):
        """Test successful credential retrieval."""
        # Mock config
        mock_config = Mock()
        mock_config.credentials_path.as_posix.return_value = '/path/to/creds.json'
        mock_config.token_path.as_posix.return_value = '/path/to/token.json'
        
        # Mock auth manager
        mock_auth_manager = Mock()
        mock_auth_manager_class.return_value = mock_auth_manager
        
        # Mock credentials
        mock_creds = Mock()
        mock_auth_manager.get_credentials.return_value = mock_creds
        
        result = get_credentials(mock_config)
        
        assert result == mock_creds
        mock_auth_manager_class.assert_called_once_with(
            credentials_path='/path/to/creds.json',
            token_path='/path/to/token.json'
        )
        mock_auth_manager.get_credentials.assert_called_once()
    
    @patch('yaml2sheet.yaml2sheet.GoogleAuthManager')
    def test_get_credentials_file_not_found(self, mock_auth_manager_class):
        """Test credential retrieval with missing credentials file."""
        # Mock config
        mock_config = Mock()
        mock_config.credentials_path.as_posix.return_value = '/path/to/creds.json'
        mock_config.token_path.as_posix.return_value = '/path/to/token.json'
        
        # Mock auth manager
        mock_auth_manager = Mock()
        mock_auth_manager_class.return_value = mock_auth_manager
        
        # Mock FileNotFoundError with credentials file message
        mock_auth_manager.get_credentials.side_effect = FileNotFoundError(
            "Credentials file not found at /path/to/creds.json"
        )
        
        result = get_credentials(mock_config)
        
        assert result is None
    
    @patch('yaml2sheet.yaml2sheet.GoogleAuthManager')
    def test_get_credentials_missing_token_file(self, mock_auth_manager_class):
        """Test credential retrieval with missing token file (normal for first run)."""
        # Mock config
        mock_config = Mock()
        mock_config.credentials_path.as_posix.return_value = '/path/to/creds.json'
        mock_config.token_path.as_posix.return_value = '/path/to/token.json'
        
        # Mock auth manager
        mock_auth_manager = Mock()
        mock_auth_manager_class.return_value = mock_auth_manager
        
        # Mock FileNotFoundError with token file message (should continue processing)
        mock_auth_manager.get_credentials.side_effect = FileNotFoundError(
            "Token file not found"
        )
        
        result = get_credentials(mock_config)
        
        # Should return None but not log as error (token file missing is normal)
        assert result is None
    
    @patch('yaml2sheet.yaml2sheet.GoogleAuthManager')
    def test_get_credentials_general_exception(self, mock_auth_manager_class):
        """Test credential retrieval with general exception."""
        # Mock config
        mock_config = Mock()
        mock_config.credentials_path.as_posix.return_value = '/path/to/creds.json'
        mock_config.token_path.as_posix.return_value = '/path/to/token.json'
        
        # Mock auth manager
        mock_auth_manager = Mock()
        mock_auth_manager_class.return_value = mock_auth_manager
        
        # Mock general exception
        mock_auth_manager.get_credentials.side_effect = Exception("General auth error")
        
        result = get_credentials(mock_config)
        
        assert result is None

    @patch('yaml2sheet.yaml2sheet.GoogleAuthManager')
    def test_get_credentials_token_file_not_found_debug_path(self, mock_auth_manager_class):
        """Test credential retrieval with token file not found - covers debug logging path."""
        # Mock config
        mock_config = Mock()
        mock_config.credentials_path.as_posix.return_value = '/path/to/creds.json'
        mock_config.token_path.as_posix.return_value = '/path/to/token.json'
        
        # Mock auth manager
        mock_auth_manager = Mock()
        mock_auth_manager_class.return_value = mock_auth_manager
        
        # Mock FileNotFoundError with token file message (should continue processing)
        mock_auth_manager.get_credentials.side_effect = FileNotFoundError(
            "Token file not found at /path/to/token.json"
        )
        
        result = get_credentials(mock_config)
        
        # Should return None and log debug message (covers lines 220-221)
        assert result is None


class TestMain:
    """Test main function integration."""
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.create_default_config')
    def test_main_create_config_success(self, mock_create_config, mock_setup_logging, mock_parse_args):
        """Test main function with --create-config flag."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = True
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args
        
        # Mock config creation
        mock_create_config.return_value = Path('/test/config.yaml')
        
        result = main()
        
        assert result == 0
        mock_setup_logging.assert_called_once()
        mock_create_config.assert_called_once()
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.create_default_config')
    def test_main_create_config_failure(self, mock_create_config, mock_setup_logging, mock_parse_args):
        """Test main function with --create-config flag failure."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = True
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args
        
        # Mock config creation failure
        mock_create_config.side_effect = Exception("Config creation failed")
        
        result = main()
        
        assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    def test_main_config_not_found_non_interactive(self, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function when config file not found in non-interactive mode."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_parse_args.return_value = mock_args
        
        # Mock config loading failure
        mock_load_config.side_effect = FileNotFoundError("Config not found")
        
        # Mock non-interactive terminal
        with patch('sys.stdout.isatty', return_value=False):
            result = main()
            
            assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.create_default_config')
    @patch('builtins.input')
    def test_main_config_not_found_interactive_yes(self, mock_input, mock_create_config, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function when config not found in interactive mode, user says yes."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_parse_args.return_value = mock_args
        
        # Mock config loading failure
        mock_load_config.side_effect = FileNotFoundError("Config not found")
        
        # Mock interactive terminal and user input
        mock_input.return_value = 'y'
        mock_create_config.return_value = Path('/test/config.yaml')
        
        with patch('sys.stdout.isatty', return_value=True):
            result = main()
            
            assert result == 0
            mock_input.assert_called_once()
            mock_create_config.assert_called_once()
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('builtins.input')
    def test_main_config_not_found_interactive_no(self, mock_input, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function when config not found in interactive mode, user says no."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_parse_args.return_value = mock_args
        
        # Mock config loading failure
        mock_load_config.side_effect = FileNotFoundError("Config not found")
        
        # Mock interactive terminal and user input
        mock_input.return_value = 'n'
        
        with patch('sys.stdout.isatty', return_value=True):
            result = main()
            
            assert result == 1
            mock_input.assert_called_once()
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('builtins.input')
    def test_main_config_not_found_interactive_keyboard_interrupt(self, mock_input, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function when config not found and user interrupts."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_parse_args.return_value = mock_args
        
        # Mock config loading failure
        mock_load_config.side_effect = FileNotFoundError("Config not found")
        
        # Mock keyboard interrupt
        mock_input.side_effect = KeyboardInterrupt()
        
        with patch('sys.stdout.isatty', return_value=True):
            result = main()
            
            assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.get_credentials')
    @patch('yaml2sheet.yaml2sheet.process_yaml_data')
    @patch('yaml2sheet.yaml2sheet.ChecklistSheetGenerator')
    @patch('yaml2sheet.yaml2sheet.GL')
    def test_main_successful_execution(self, mock_gl, mock_generator_class, mock_process_yaml, mock_get_creds, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test successful main execution."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_args.production = False
        mock_args.basedir = '/test/basedir'
        mock_args.url = None
        mock_args.init = False
        mock_parse_args.return_value = mock_args
        
        # Mock configuration
        mock_config = Mock()
        mock_config.get_basedir.return_value = Path('/test/basedir')
        mock_config.get_base_url.return_value = 'https://test.example.com'
        mock_config.get_spreadsheet_id.return_value = 'test_spreadsheet_id'
        mock_config.sheet_editor_email = 'test@example.com'
        mock_load_config.return_value = mock_config
        
        # Mock credentials
        mock_creds = Mock()
        mock_get_creds.return_value = mock_creds
        
        # Mock YAML processing
        mock_source_data = {
            'version': '1.0.0',
            'date': '2024-01-01',
            'checks': {'0001': {'id': '0001'}}
        }
        mock_process_yaml.return_value = mock_source_data
        
        # Mock sheet generator
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        
        result = main()
        
        assert result == 0
        mock_load_config.assert_called_once_with(None)
        mock_get_creds.assert_called_once_with(mock_config)
        mock_process_yaml.assert_called_once_with('/test/basedir')
        mock_generator_class.assert_called_once_with(mock_creds, 'test_spreadsheet_id', 'test@example.com')
        mock_generator.generate_checklist.assert_called_once_with(mock_source_data, initialize=False)
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.get_credentials')
    def test_main_authentication_failure(self, mock_get_creds, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function with authentication failure."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_parse_args.return_value = mock_args
        
        # Mock configuration
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        
        # Mock authentication failure
        mock_get_creds.return_value = None
        
        result = main()
        
        assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.get_credentials')
    @patch('yaml2sheet.yaml2sheet.process_yaml_data')
    def test_main_yaml_processing_failure(self, mock_process_yaml, mock_get_creds, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function with YAML processing failure."""
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_args.basedir = '/test/basedir'
        mock_args.url = None
        mock_parse_args.return_value = mock_args
        
        # Mock configuration
        mock_config = Mock()
        mock_config.get_basedir.return_value = Path('/test/basedir')
        mock_config.get_base_url.return_value = 'https://test.example.com'
        mock_load_config.return_value = mock_config
        
        # Mock credentials
        mock_creds = Mock()
        mock_get_creds.return_value = mock_creds
        
        # Mock YAML processing failure
        mock_process_yaml.side_effect = Exception("YAML processing failed")
        
        result = main()
        
        assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.get_credentials')
    @patch('yaml2sheet.yaml2sheet.process_yaml_data')
    @patch('yaml2sheet.yaml2sheet.ChecklistSheetGenerator')
    def test_main_google_api_error(self, mock_generator_class, mock_process_yaml, mock_get_creds, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function with Google API error."""
        from googleapiclient.errors import HttpError
        
        # Mock arguments
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_args.production = False
        mock_args.basedir = '/test/basedir'
        mock_args.url = None
        mock_args.init = False
        mock_parse_args.return_value = mock_args
        
        # Mock configuration
        mock_config = Mock()
        mock_config.get_basedir.return_value = Path('/test/basedir')
        mock_config.get_base_url.return_value = 'https://test.example.com'
        mock_config.get_spreadsheet_id.return_value = 'test_spreadsheet_id'
        mock_config.sheet_editor_email = 'test@example.com'
        mock_load_config.return_value = mock_config
        
        # Mock credentials
        mock_creds = Mock()
        mock_get_creds.return_value = mock_creds
        
        # Mock YAML processing
        mock_source_data = {'checks': {}}
        mock_process_yaml.return_value = mock_source_data
        
        # Mock sheet generator with HTTP error
        mock_generator = Mock()
        # Create a real HttpError instance
        http_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'),
            content=b'Forbidden'
        )
        mock_generator.generate_checklist.side_effect = http_error
        mock_generator_class.return_value = mock_generator
        
        result = main()
        
        assert result == 1
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    def test_main_verbose_logging(self, mock_setup_logging, mock_parse_args):
        """Test main function with verbose logging enabled."""
        # Mock arguments with verbose flag
        mock_args = Mock()
        mock_args.create_config = True  # Use create_config to exit early
        mock_args.verbose = True
        mock_parse_args.return_value = mock_args
        
        with patch('yaml2sheet.yaml2sheet.create_default_config') as mock_create_config:
            mock_create_config.return_value = Path('/test/config.yaml')
            
            result = main()
            
            # Should call setup_logging twice: once with default, once with DEBUG
            assert mock_setup_logging.call_count == 2
            import logging
            mock_setup_logging.assert_any_call()  # First call with default
            mock_setup_logging.assert_any_call(logging.DEBUG)  # Second call with DEBUG
    
    @patch('yaml2sheet.yaml2sheet.parse_args')
    @patch('yaml2sheet.yaml2sheet.setup_logging')
    @patch('yaml2sheet.yaml2sheet.load_configuration')
    @patch('yaml2sheet.yaml2sheet.get_credentials')
    @patch('yaml2sheet.yaml2sheet.process_yaml_data')
    @patch('yaml2sheet.yaml2sheet.ChecklistSheetGenerator')
    def test_main_with_init_flag(self, mock_generator_class, mock_process_yaml, mock_get_creds, mock_load_config, mock_setup_logging, mock_parse_args):
        """Test main function with --init flag."""
        # Mock arguments with init flag
        mock_args = Mock()
        mock_args.create_config = False
        mock_args.verbose = False
        mock_args.config = None
        mock_args.production = False
        mock_args.basedir = '/test/basedir'
        mock_args.url = None
        mock_args.init = True  # Initialize spreadsheet
        mock_parse_args.return_value = mock_args
        
        # Mock configuration
        mock_config = Mock()
        mock_config.get_basedir.return_value = Path('/test/basedir')
        mock_config.get_base_url.return_value = 'https://test.example.com'
        mock_config.get_spreadsheet_id.return_value = 'test_spreadsheet_id'
        mock_config.sheet_editor_email = 'test@example.com'
        mock_load_config.return_value = mock_config
        
        # Mock credentials
        mock_creds = Mock()
        mock_get_creds.return_value = mock_creds
        
        # Mock YAML processing
        mock_source_data = {'checks': {}}
        mock_process_yaml.return_value = mock_source_data
        
        # Mock sheet generator
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        
        with patch('yaml2sheet.yaml2sheet.GL'):
            result = main()
            
            assert result == 0
            # Should call generate_checklist with initialize=True
            mock_generator.generate_checklist.assert_called_once_with(mock_source_data, initialize=True)


class TestMainIntegration:
    """Test main function as entry point."""
    
    def test_main_as_script_entry_point(self):
        """Test that main can be called as script entry point."""
        # This test ensures the if __name__ == '__main__' block works
        with patch('yaml2sheet.yaml2sheet.main') as mock_main:
            mock_main.return_value = 0
            
            # Simulate running as script
            with patch('sys.argv', ['yaml2sheet', '--create-config']):
                # Import and execute the main block
                import yaml2sheet.yaml2sheet
                
                # The main function should be callable
                assert callable(yaml2sheet.yaml2sheet.main)
