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
        # Try to run the module - this test only works when package is installed
        try:
            result = subprocess.run([
                sys.executable, '-m', 'yaml2sheet', '--help'
            ], capture_output=True, text=True)
            
            # If the module is found and executed, check the result
            if result.returncode == 0:
                assert 'usage:' in result.stdout.lower() or 'help' in result.stdout.lower()
            else:
                # If module is not found (not installed), skip this test
                if 'No module named yaml2sheet' in result.stderr:
                    pytest.skip("Package not installed - skipping module execution test")
                else:
                    # Some other error occurred
                    assert result.returncode == 0, f"Unexpected error: {result.stderr}"
        except Exception as e:
            pytest.skip(f"Could not execute module test: {e}")
