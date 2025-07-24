"""Tests for version_utils module."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from freee_a11y_gl.version_utils import get_version_info, VersionError


class TestGetVersionInfo:
    """Test cases for get_version_info function."""

    def test_get_version_info_with_valid_version_file(self):
        """Test get_version_info with a valid version.py file."""
        version_content = '''# Version information
__version__ = "1.2.3"
__author__ = "Test Author"
__email__ = "test@example.com"
release_date = "2023-01-01"
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '1.2.3'
            assert result['__author__'] == 'Test Author'
            assert result['__email__'] == 'test@example.com'
            assert result['release_date'] == '2023-01-01'

    def test_get_version_info_with_single_quotes(self):
        """Test get_version_info handles single quotes in values."""
        version_content = '''__version__ = '2.0.0'
__author__ = 'Single Quote Author'
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '2.0.0'
            assert result['__author__'] == 'Single Quote Author'

    def test_get_version_info_with_comments_and_empty_lines(self):
        """Test get_version_info ignores comments and empty lines."""
        version_content = '''# This is a comment
# Another comment

__version__ = "1.0.0"

# More comments
__author__ = "Test Author"

# Final comment
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '1.0.0'
            assert result['__author__'] == 'Test Author'
            assert len(result) == 2  # Only non-comment lines

    def test_get_version_info_missing_version_file(self):
        """Test get_version_info raises error when version.py is missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(VersionError) as exc_info:
                get_version_info(basedir=temp_dir)
            
            assert 'Version file not found' in str(exc_info.value)

    def test_get_version_info_empty_version_file(self):
        """Test get_version_info with empty version file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write('')
            
            result = get_version_info(basedir=temp_dir)
            
            assert result == {}

    def test_get_version_info_only_comments(self):
        """Test get_version_info with file containing only comments."""
        version_content = '''# Only comments here
# No actual version data
# Just comments
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result == {}

    def test_get_version_info_malformed_lines(self):
        """Test get_version_info handles malformed lines gracefully."""
        version_content = '''__version__ = "1.0.0"
malformed_line_without_equals
__author__ = "Test Author"
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            # Should skip malformed lines and process valid ones
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '1.0.0'
            assert result['__author__'] == 'Test Author'
            assert len(result) == 2  # Only valid lines processed

    def test_get_version_info_with_spaces_in_assignment(self):
        """Test get_version_info handles various spacing in assignments."""
        version_content = '''__version__="1.0.0"
__author__ = "Test Author"
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            # Should raise VersionError due to malformed line (no space around =)
            with pytest.raises(VersionError, match="Failed to read version information"):
                result = get_version_info(basedir=temp_dir)

    @patch('freee_a11y_gl.config.Config')
    def test_get_version_info_uses_config_default(self, mock_config):
        """Test get_version_info uses Config default when basedir is None."""
        version_content = '__version__ = "1.0.0"'
        
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_config.get_basedir.return_value = temp_dir
            
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info()
            
            mock_config.get_basedir.assert_called_once()
            assert result['__version__'] == '1.0.0'

    def test_get_version_info_file_permission_error(self):
        """Test get_version_info handles file permission errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            version_file.touch()
            
            # Mock open to raise PermissionError
            with patch('builtins.open', side_effect=PermissionError("Permission denied")):
                with pytest.raises(VersionError) as exc_info:
                    get_version_info(basedir=temp_dir)
                
                assert 'Failed to read version information' in str(exc_info.value)

    def test_get_version_info_unicode_content(self):
        """Test get_version_info handles Unicode content correctly."""
        version_content = '''__version__ = "1.0.0"
__author__ = "テスト作者"
__description__ = "日本語の説明"
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '1.0.0'
            assert result['__author__'] == 'テスト作者'
            assert result['__description__'] == '日本語の説明'

    def test_get_version_info_mixed_quote_types(self):
        """Test get_version_info handles mixed quote types."""
        version_content = '''__version__ = "1.0.0"
__author__ = 'Single Quote Author'
__email__ = "double@example.com"
__license__ = 'MIT'
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            version_file = Path(temp_dir) / 'version.py'
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            
            result = get_version_info(basedir=temp_dir)
            
            assert result['__version__'] == '1.0.0'
            assert result['__author__'] == 'Single Quote Author'
            assert result['__email__'] == 'double@example.com'
            assert result['__license__'] == 'MIT'


class TestVersionError:
    """Test cases for VersionError exception."""

    def test_version_error_creation(self):
        """Test VersionError can be created and raised."""
        error_msg = "Test version error"
        
        with pytest.raises(VersionError) as exc_info:
            raise VersionError(error_msg)
        
        assert str(exc_info.value) == error_msg

    def test_version_error_inheritance(self):
        """Test VersionError inherits from Exception."""
        error = VersionError("test")
        assert isinstance(error, Exception)

    def test_version_error_with_nested_exception(self):
        """Test VersionError can wrap other exceptions."""
        original_error = FileNotFoundError("Original error")
        version_error = VersionError(f"Wrapped error: {str(original_error)}")
        
        with pytest.raises(VersionError) as exc_info:
            raise version_error
        
        assert "Wrapped error: Original error" in str(exc_info.value)
