import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.utils import join_items, uniq, tag2sc


class TestJoinItems:
    """Test cases for join_items function."""

    @patch('freee_a11y_gl.utils.Config')
    def test_join_items_single_platform_ja(self, mock_config):
        """Test joining single platform item in Japanese."""
        mock_config.get_list_separator.return_value = "、"
        mock_config.get_platform_name.return_value = "Web"
        
        result = join_items(["web"], "ja")
        
        mock_config.get_list_separator.assert_called_once_with("ja")
        mock_config.get_platform_name.assert_called_once_with("web", "ja")
        assert result == "Web"

    @patch('freee_a11y_gl.utils.Config')
    def test_join_items_multiple_platforms_ja(self, mock_config):
        """Test joining multiple platform items in Japanese."""
        mock_config.get_list_separator.return_value = "、"
        mock_config.get_platform_name.side_effect = lambda item, lang: {
            "web": "Web",
            "mobile": "モバイル"
        }[item]
        
        result = join_items(["web", "mobile"], "ja")
        
        mock_config.get_list_separator.assert_called_once_with("ja")
        assert mock_config.get_platform_name.call_count == 2
        assert result == "Web、モバイル"

    @patch('freee_a11y_gl.utils.Config')
    def test_join_items_multiple_platforms_en(self, mock_config):
        """Test joining multiple platform items in English."""
        mock_config.get_list_separator.return_value = ", "
        mock_config.get_platform_name.side_effect = lambda item, lang: {
            "web": "Web",
            "mobile": "Mobile"
        }[item]
        
        result = join_items(["web", "mobile"], "en")
        
        mock_config.get_list_separator.assert_called_once_with("en")
        assert mock_config.get_platform_name.call_count == 2
        assert result == "Web, Mobile"

    @patch('freee_a11y_gl.utils.Config')
    def test_join_items_empty_list(self, mock_config):
        """Test joining empty list."""
        mock_config.get_list_separator.return_value = "、"
        
        result = join_items([], "ja")
        
        mock_config.get_list_separator.assert_called_once_with("ja")
        assert result == ""

    @patch('freee_a11y_gl.utils.Config')
    def test_join_items_three_platforms(self, mock_config):
        """Test joining three platform items."""
        mock_config.get_list_separator.return_value = ", "
        mock_config.get_platform_name.side_effect = lambda item, lang: {
            "web": "Web",
            "ios": "iOS", 
            "android": "Android"
        }[item]
        
        result = join_items(["web", "ios", "android"], "en")
        
        assert result == "Web, iOS, Android"


class TestUniq:
    """Test cases for uniq function."""

    def test_uniq_list_with_duplicates(self):
        """Test removing duplicates from list."""
        input_list = [1, 2, 3, 2, 4, 1, 5]
        result = uniq(input_list)
        assert result == [1, 2, 3, 4, 5]

    def test_uniq_list_no_duplicates(self):
        """Test list with no duplicates."""
        input_list = [1, 2, 3, 4, 5]
        result = uniq(input_list)
        assert result == input_list

    def test_uniq_empty_list(self):
        """Test empty list."""
        result = uniq([])
        assert result == []

    def test_uniq_single_item(self):
        """Test single item list."""
        input_list = [1]
        result = uniq(input_list)
        assert result == input_list

    def test_uniq_all_same_items(self):
        """Test list with all same items."""
        result = uniq([1, 1, 1, 1])
        assert result == [1]

    def test_uniq_string_list(self):
        """Test string list with duplicates."""
        input_list = ["a", "b", "c", "b", "d", "a"]
        result = uniq(input_list)
        assert result == ["a", "b", "c", "d"]

    def test_uniq_tuple_input(self):
        """Test tuple input."""
        input_tuple = (1, 2, 3, 2, 4, 1)
        result = uniq(input_tuple)
        assert result == [1, 2, 3, 4]

    def test_uniq_preserves_order(self):
        """Test that original order is preserved."""
        input_list = ["first", "second", "third", "second", "fourth", "first"]
        result = uniq(input_list)
        assert result == ["first", "second", "third", "fourth"]

    def test_uniq_mixed_types(self):
        """Test mixed types in sequence."""
        input_list = [1, "a", 2, "a", 1, 3]
        result = uniq(input_list)
        assert result == [1, "a", 2, 3]


class TestTag2sc:
    """Test cases for tag2sc function."""

    def test_tag2sc_basic_pattern(self):
        """Test basic WCAG tag conversion."""
        result = tag2sc("wcag111")
        assert result == "1.1.1"

    def test_tag2sc_double_digit_level(self):
        """Test conversion with double digit level."""
        result = tag2sc("wcag2410")
        assert result == "2.4.10"

    def test_tag2sc_triple_digit_level(self):
        """Test conversion with triple digit level."""
        result = tag2sc("wcag21123")
        assert result == "2.1.123"

    def test_tag2sc_different_principle(self):
        """Test conversion with different principle numbers."""
        result = tag2sc("wcag321")
        assert result == "3.2.1"

    def test_tag2sc_different_guideline(self):
        """Test conversion with different guideline numbers."""
        result = tag2sc("wcag141")
        assert result == "1.4.1"

    def test_tag2sc_no_match(self):
        """Test tag that doesn't match pattern."""
        text = "not-wcag-tag"
        result = tag2sc(text)
        assert result == text

    def test_tag2sc_partial_match(self):
        """Test tag with partial match."""
        text = "wcag-incomplete"
        result = tag2sc(text)
        assert result == text

    def test_tag2sc_empty_string(self):
        """Test empty string input."""
        text = ""
        result = tag2sc(text)
        assert result == text

    def test_tag2sc_multiple_matches(self):
        """Test string with multiple WCAG patterns."""
        result = tag2sc("wcag111-wcag212")
        assert result == "1.1.1-2.1.2"

    def test_tag2sc_case_sensitivity(self):
        """Test case sensitivity."""
        result = tag2sc("WCAG111")
        assert result == "WCAG111"  # Should not match due to case
        
        result = tag2sc("wcag111")
        assert result == "1.1.1"  # Should match lowercase
