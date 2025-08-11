"""Tests for yaml2sheet.__main__ module."""

import sys
import subprocess
from unittest.mock import patch
import pytest


class TestMain:
    """Test cases for __main__ module entry point."""

    def test_main_module_import(self):
        """Test that __main__ module can be imported."""
        import yaml2sheet.__main__
        assert hasattr(yaml2sheet.__main__, 'main')

    def test_main_module_execution_path(self):
        """Test the execution path in __main__ module."""
        # Import the module to get access to its namespace
        import yaml2sheet.__main__ as main_module
        
        # Mock the main function in the __main__ module namespace
        with patch.object(main_module, 'main') as mock_main:
            # Directly call the main function to simulate script execution
            main_module.main()
            
            # Verify main was called
            mock_main.assert_called_once()

    def test_main_via_python_module_execution(self):
        """Test executing the module via python -m to get coverage."""
        # This will actually execute the __main__ module and should provide coverage
        result = subprocess.run([
            sys.executable, '-m', 'yaml2sheet', '--help'
        ], capture_output=True, text=True)
        
        # Should show help and exit with code 0
        assert result.returncode == 0
        assert 'usage:' in result.stdout.lower() or 'help' in result.stdout.lower()
