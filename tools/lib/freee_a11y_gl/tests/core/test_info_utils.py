"""Tests for info_utils module."""

import pytest
import pickle
import tempfile
from pathlib import Path
from unittest.mock import patch

from freee_a11y_gl.info_utils import get_info_links, InfoUtilsError


class MockDoctree:
    """Mock doctree object that can be pickled."""
    def __init__(self, labels_dict):
        self.domaindata = {
            'std': {
                'labels': labels_dict
            }
        }


class TestGetInfoLinks:
    """Test cases for get_info_links function."""

    def test_get_info_links_with_valid_pickle_files(self):
        """Test get_info_links with valid pickle files."""
        labels_dict = {
            'test-label': ['page', 'anchor', 'Test Label Text'],
            'another-label': ['another-page', 'another-anchor', 'Another Label']
        }
        mock_doctree = MockDoctree(labels_dict)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory structure
            ja_dir = Path(temp_dir) / 'ja' / 'build' / 'doctrees'
            en_dir = Path(temp_dir) / 'en' / 'build' / 'doctrees'
            ja_dir.mkdir(parents=True)
            en_dir.mkdir(parents=True)
            
            # Create pickle files
            ja_pickle = ja_dir / 'environment.pickle'
            en_pickle = en_dir / 'environment.pickle'
            
            with open(ja_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            with open(en_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            
            # Test the function
            result = get_info_links(basedir=temp_dir, baseurl='https://example.com')
            
            assert 'test-label' in result
            assert 'another-label' in result
            
            # Check structure
            assert 'text' in result['test-label']
            assert 'url' in result['test-label']
            assert 'ja' in result['test-label']['text']
            assert 'en' in result['test-label']['text']
            
            # Check values
            assert result['test-label']['text']['ja'] == 'Test Label Text'
            assert result['test-label']['text']['en'] == 'Test Label Text'
            assert result['test-label']['url']['ja'] == 'https://example.com/page.html#anchor'
            assert result['test-label']['url']['en'] == 'https://example.com/en/page.html#anchor'

    def test_get_info_links_with_incomplete_labels(self):
        """Test get_info_links filters out incomplete labels."""
        labels_dict = {
            'complete-label': ['page', 'anchor', 'Complete Label'],
            'incomplete-label-1': ['page', '', 'Missing anchor'],
            'incomplete-label-2': ['', 'anchor', 'Missing page'],
            'incomplete-label-3': ['page', 'anchor', ''],  # Missing text
            'another-complete': ['page2', 'anchor2', 'Another Complete']
        }
        mock_doctree = MockDoctree(labels_dict)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            ja_dir = Path(temp_dir) / 'ja' / 'build' / 'doctrees'
            en_dir = Path(temp_dir) / 'en' / 'build' / 'doctrees'
            ja_dir.mkdir(parents=True)
            en_dir.mkdir(parents=True)
            
            ja_pickle = ja_dir / 'environment.pickle'
            en_pickle = en_dir / 'environment.pickle'
            
            with open(ja_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            with open(en_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            
            result = get_info_links(basedir=temp_dir, baseurl='https://example.com')
            
            # Only complete labels should be included
            assert 'complete-label' in result
            assert 'another-complete' in result
            assert 'incomplete-label-1' not in result
            assert 'incomplete-label-2' not in result
            assert 'incomplete-label-3' not in result

    def test_get_info_links_missing_pickle_file(self):
        """Test get_info_links raises error when pickle file is missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(InfoUtilsError) as exc_info:
                get_info_links(basedir=temp_dir, baseurl='https://example.com')
            
            assert 'Failed to load pickle file' in str(exc_info.value)

    def test_get_info_links_corrupted_pickle_file(self):
        """Test get_info_links raises error when pickle file is corrupted."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ja_dir = Path(temp_dir) / 'ja' / 'build' / 'doctrees'
            ja_dir.mkdir(parents=True)
            
            # Create corrupted pickle file
            ja_pickle = ja_dir / 'environment.pickle'
            with open(ja_pickle, 'w') as f:
                f.write('corrupted data')
            
            with pytest.raises(InfoUtilsError) as exc_info:
                get_info_links(basedir=temp_dir, baseurl='https://example.com')
            
            assert 'Failed to load pickle file' in str(exc_info.value)

    @patch('freee_a11y_gl.config.Config')
    def test_get_info_links_uses_config_defaults(self, mock_config):
        """Test get_info_links uses Config defaults when parameters are None."""
        labels_dict = {
            'test-label': ['page', 'anchor', 'Test Label']
        }
        mock_doctree = MockDoctree(labels_dict)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override the config return values to use our temp directory
            mock_config.get_basedir.return_value = temp_dir
            mock_config.get_base_url.return_value = 'https://default.url'
            
            ja_dir = Path(temp_dir) / 'ja' / 'build' / 'doctrees'
            en_dir = Path(temp_dir) / 'en' / 'build' / 'doctrees'
            ja_dir.mkdir(parents=True)
            en_dir.mkdir(parents=True)
            
            ja_pickle = ja_dir / 'environment.pickle'
            en_pickle = en_dir / 'environment.pickle'
            
            with open(ja_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            with open(en_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            
            # Call without parameters to test defaults
            result = get_info_links()
            
            # Verify Config methods were called
            mock_config.get_basedir.assert_called_once()
            mock_config.get_base_url.assert_called_once_with(None)
            
            # Verify result structure
            assert 'test-label' in result

    def test_get_info_links_empty_labels(self):
        """Test get_info_links with empty labels dictionary."""
        labels_dict = {}
        mock_doctree = MockDoctree(labels_dict)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            ja_dir = Path(temp_dir) / 'ja' / 'build' / 'doctrees'
            en_dir = Path(temp_dir) / 'en' / 'build' / 'doctrees'
            ja_dir.mkdir(parents=True)
            en_dir.mkdir(parents=True)
            
            ja_pickle = ja_dir / 'environment.pickle'
            en_pickle = en_dir / 'environment.pickle'
            
            with open(ja_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            with open(en_pickle, 'wb') as f:
                pickle.dump(mock_doctree, f)
            
            result = get_info_links(basedir=temp_dir, baseurl='https://example.com')
            
            assert result == {}


class TestInfoUtilsError:
    """Test cases for InfoUtilsError exception."""

    def test_info_utils_error_creation(self):
        """Test InfoUtilsError can be created and raised."""
        error_msg = "Test error message"
        
        with pytest.raises(InfoUtilsError) as exc_info:
            raise InfoUtilsError(error_msg)
        
        assert str(exc_info.value) == error_msg

    def test_info_utils_error_inheritance(self):
        """Test InfoUtilsError inherits from Exception."""
        error = InfoUtilsError("test")
        assert isinstance(error, Exception)
