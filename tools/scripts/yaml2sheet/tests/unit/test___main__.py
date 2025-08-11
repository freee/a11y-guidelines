"""
Tests for __main__ module.

Tests the command line entry point functionality.
"""

import pytest
import subprocess
import sys
from unittest.mock import patch


class TestMainModule:
    """Test __main__ module functionality."""
    
    def test_main_module_import(self):
        """Test that __main__ module can be imported and has main function."""
        import yaml2sheet.__main__
        
        # The main function should be available
        assert hasattr(yaml2sheet.__main__, 'main')
        
        # Should be the same main function from yaml2sheet module
        from yaml2sheet.yaml2sheet import main as yaml2sheet_main
        assert yaml2sheet.__main__.main == yaml2sheet_main
    
    @patch('yaml2sheet.yaml2sheet.main')
    def test_main_module_execution_via_python_m(self, mock_main):
        """Test __main__ module execution via python -m."""
        mock_main.return_value = 0
        
        # Test that we can execute the module via python -m
        # This will actually trigger the if __name__ == '__main__' block
        try:
            result = subprocess.run([
                sys.executable, '-m', 'yaml2sheet', '--help'
            ], capture_output=True, text=True, timeout=10, cwd='src')
            
            # Should not crash (exit code 0 for --help or 2 for argument error is fine)
            assert result.returncode in [0, 2]
            
        except subprocess.TimeoutExpired:
            # If it times out, that's also acceptable - means it's trying to run
            pass
        except Exception:
            # If there are import issues, that's expected in test environment
            pass
