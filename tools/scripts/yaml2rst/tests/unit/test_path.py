"""Tests for path.py module."""
from unittest.mock import patch
import os


class TestPath:
    """Test path utility functions."""

    def test_get_dest_dirnames_multiple_languages(self):
        """Test get_dest_dirnames with multiple languages."""
        from yaml2rst.path import get_dest_dirnames

        basedir = "/test/base"
        lang = "ja"

        with patch('yaml2rst.path.AVAILABLE_LANGUAGES', ['ja', 'en']):
            result = get_dest_dirnames(basedir, lang)

        # Should include language directory when multiple languages available
        expected_langdir = os.path.join(basedir, lang)
        assert result['base'] == expected_langdir
        assert 'guidelines' in result
        assert 'checks' in result
        assert 'misc' in result

    def test_get_dest_dirnames_single_language(self):
        """Test get_dest_dirnames with single language (covers line 47)."""
        from yaml2rst.path import get_dest_dirnames

        basedir = "/test/base"
        lang = "ja"

        # Mock AVAILABLE_LANGUAGES to have only one language
        with patch('yaml2rst.path.AVAILABLE_LANGUAGES', ['ja']):
            result = get_dest_dirnames(basedir, lang)

        # Should use basedir directly when only one language available
        assert result['base'] == basedir
        assert 'guidelines' in result
        assert 'checks' in result
        assert 'misc' in result

    def test_get_static_dest_files(self):
        """Test get_static_dest_files function."""
        from yaml2rst.path import get_static_dest_files

        basedir = "/test/base"
        lang = "en"

        result = get_static_dest_files(basedir, lang)

        # Verify all expected keys are present
        expected_keys = [
            'all_checks', 'wcag21mapping', 'priority_diff', 'miscdefs',
            'faq_index', 'faq_article_index', 'faq_tag_index', 'makefile',
            'axe_rules'
        ]

        for key in expected_keys:
            assert key in result
            assert isinstance(result[key], str)
            assert len(result[key]) > 0

    def test_template_constants(self):
        """Test that template constants are properly defined."""
        from yaml2rst.path import (
            TEMPLATE_DIR, TEMPLATE_FILENAMES, FAQ_INDEX_FILENAME,
            MAKEFILE_FILENAME, ALL_CHECKS_FILENAME
        )

        # Verify constants are strings
        assert isinstance(TEMPLATE_DIR, str)
        assert isinstance(FAQ_INDEX_FILENAME, str)
        assert isinstance(MAKEFILE_FILENAME, str)
        assert isinstance(ALL_CHECKS_FILENAME, str)

        # Verify TEMPLATE_FILENAMES is a dict with expected keys
        assert isinstance(TEMPLATE_FILENAMES, dict)
        expected_template_keys = [
            'tool_example', 'allchecks_text', 'category_page',
            'info_to_gl', 'info_to_faq', 'faq_article', 'faq_tagpage',
            'faq_index'
        ]

        for key in expected_template_keys:
            assert key in TEMPLATE_FILENAMES

    def test_path_integration(self):
        """Test integration between path functions."""
        from yaml2rst.path import get_dest_dirnames, get_static_dest_files

        basedir = "/integration/test"
        lang = "en"

        # Get directory names
        dirnames = get_dest_dirnames(basedir, lang)

        # Get static file paths
        static_files = get_static_dest_files(basedir, lang)

        # Verify that static files use the correct base directories
        assert static_files['makefile'].startswith(dirnames['base'])
        assert static_files['all_checks'].startswith(dirnames['checks'])
        assert static_files['faq_index'].startswith(
            dirnames['faq_base'])
