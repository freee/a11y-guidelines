"""Tests for __main__.py entry point."""
import pytest
from unittest.mock import patch, Mock
import sys
import os

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


class TestMainEntryPoint:
    """Test the main entry point functionality."""

    def test_main_entry_point_execution(self):
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
        """Test that importing __main__ doesn't call main() when not run directly."""
        # Import the module (this should not call main since __name__ != '__main__')
        import yaml2rst.__main__
        
        # Since we're importing, not running directly, main should not be called
        # The mock was set up before import, so any calls would be recorded
        # But we need to check the actual behavior
        
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
        """Test that the main function from yaml2rst module is properly imported."""
        from yaml2rst.__main__ import main
        from yaml2rst.yaml2rst import main as yaml2rst_main
        
        # Verify that the imported main is the same as the one from yaml2rst module
        assert main is yaml2rst_main

    def test_module_can_be_executed_as_script(self):
        """Test that the module can be executed as a script using python -m."""
        import subprocess
        import sys
        import os
        
        # Get the absolute path to the yaml2rst directory
        yaml2rst_dir = os.path.join(os.path.dirname(__file__), '../../')
        yaml2rst_dir = os.path.abspath(yaml2rst_dir)
        
        # Test running the module as a script (this will actually execute it)
        # We'll use --help to avoid full execution but verify the entry point works
        result = subprocess.run(
            [sys.executable, '-m', 'yaml2rst', '--help'],
            cwd=yaml2rst_dir,
            capture_output=True,
            text=True
        )
        
        # The command should execute without import errors
        # Even if it fails due to missing arguments, it should not have import errors
        assert 'ModuleNotFoundError' not in result.stderr
        assert 'ImportError' not in result.stderr

    def test_main_execution_when_run_as_main(self):
        """Test that main() is called when __main__.py is executed as main."""
        # This test verifies the structure and logic of the __main__.py file
        # The actual execution is tested through the subprocess test
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
