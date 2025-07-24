"""Tests for source module."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

from freee_a11y_gl.source import get_src_path


class TestGetSrcPath:
    """Test cases for get_src_path function."""

    def test_get_src_path_with_valid_basedir(self):
        """Test get_src_path with a valid base directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(temp_dir)
            
            # Check that all expected paths are returned
            assert 'checks' in result
            assert 'guidelines' in result
            assert 'faq' in result
            assert 'gl_categories' in result
            assert 'wcag_sc' in result
            assert 'faq_tags' in result
            assert 'info' in result
            
            # Check path correctness
            assert str(result['checks']).endswith('data/yaml/checks')
            assert str(result['guidelines']).endswith('data/yaml/gl')
            assert str(result['faq']).endswith('data/yaml/faq')
            assert str(result['gl_categories']).endswith('data/json/guideline-categories.json')
            assert str(result['wcag_sc']).endswith('data/json/wcag-sc.json')
            assert str(result['faq_tags']).endswith('data/json/faq-tags.json')
            assert str(result['info']).endswith('data/json/info.json')

    @patch('freee_a11y_gl.config.Config')
    def test_get_src_path_with_none_basedir(self, mock_config):
        """Test get_src_path uses Config default when basedir is None."""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_config.get_basedir.return_value = temp_dir
            
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(None)
            
            # Verify Config was called
            mock_config.get_basedir.assert_called_once()
            
            # Check that paths are returned
            assert 'checks' in result
            assert 'guidelines' in result
            assert 'faq' in result

    def test_get_src_path_path_construction(self):
        """Test get_src_path constructs paths correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(temp_dir)
            
            # Test specific path construction
            expected_checks = os.path.join(temp_dir, 'data', 'yaml', 'checks')
            expected_guidelines = os.path.join(temp_dir, 'data', 'yaml', 'gl')
            expected_faq = os.path.join(temp_dir, 'data', 'yaml', 'faq')
            expected_gl_categories = os.path.join(temp_dir, 'data', 'json', 'guideline-categories.json')
            expected_wcag_sc = os.path.join(temp_dir, 'data', 'json', 'wcag-sc.json')
            expected_faq_tags = os.path.join(temp_dir, 'data', 'json', 'faq-tags.json')
            expected_info = os.path.join(temp_dir, 'data', 'json', 'info.json')
            
            assert result['checks'] == expected_checks
            assert result['guidelines'] == expected_guidelines
            assert result['faq'] == expected_faq
            assert result['gl_categories'] == expected_gl_categories
            assert result['wcag_sc'] == expected_wcag_sc
            assert result['faq_tags'] == expected_faq_tags
            assert result['info'] == expected_info

    def test_get_src_path_return_type(self):
        """Test get_src_path returns correct data types."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create minimal directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(temp_dir)
            
            # Check return type is dictionary
            assert isinstance(result, dict)
            
            # Check all values are strings
            for key, path in result.items():
                assert isinstance(path, str), f"Expected string for {key}, got {type(path)}"

    def test_get_src_path_with_string_basedir(self):
        """Test get_src_path works with string basedir."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            # Pass string instead of Path
            result = get_src_path(str(temp_dir))
            
            # Should still work correctly
            assert 'checks' in result
            assert 'guidelines' in result
            assert isinstance(result['checks'], str)

    def test_get_src_path_with_path_object_basedir(self):
        """Test get_src_path works with Path object basedir."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            # Pass Path object
            result = get_src_path(Path(temp_dir))
            
            # Should work correctly
            assert 'checks' in result
            assert 'guidelines' in result
            assert isinstance(result['checks'], str)

    def test_get_src_path_all_expected_keys(self):
        """Test get_src_path returns all expected keys."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(temp_dir)
            
            expected_keys = {
                'checks', 'guidelines', 'faq', 
                'gl_categories', 'wcag_sc', 'faq_tags', 'info'
            }
            
            assert set(result.keys()) == expected_keys

    def test_get_src_path_directory_vs_file_paths(self):
        """Test get_src_path correctly distinguishes directories from files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create expected directory structure
            data_dir = Path(temp_dir) / 'data'
            json_dir = data_dir / 'json'
            yaml_dir = data_dir / 'yaml'
            
            data_dir.mkdir()
            json_dir.mkdir()
            yaml_dir.mkdir()
            
            # Create subdirectories
            (yaml_dir / 'checks').mkdir()
            (yaml_dir / 'gl').mkdir()
            (yaml_dir / 'faq').mkdir()
            
            # Create expected JSON files
            (json_dir / 'guideline-categories.json').touch()
            (json_dir / 'wcag-sc.json').touch()
            (json_dir / 'faq-tags.json').touch()
            (json_dir / 'info.json').touch()
            
            result = get_src_path(temp_dir)
            
            # Directory paths
            directory_keys = ['checks', 'guidelines', 'faq']
            for key in directory_keys:
                assert Path(result[key]).is_dir(), f"{key} should be a directory"
            
            # File paths
            file_keys = ['gl_categories', 'wcag_sc', 'faq_tags', 'info']
            for key in file_keys:
                assert Path(result[key]).is_file(), f"{key} should be a file"
