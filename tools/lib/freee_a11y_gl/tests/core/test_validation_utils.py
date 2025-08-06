"""Tests for input validation utilities."""
import pytest

from freee_a11y_gl.validation_utils import InputValidator
from freee_a11y_gl.exceptions import ValidationError


class TestInputValidator:
    """Test cases for InputValidator class."""

    @pytest.mark.parametrize("valid_id", [
        "test", "test123", "test-id", "test_id", "TEST_ID-123", "a1", "123"
    ])
    def test_validate_id_valid(self, valid_id):
        """Test validate_id with valid IDs."""
        result = InputValidator.validate_id(valid_id)
        assert result == valid_id

    @pytest.mark.parametrize("invalid_id,reason", [
        ("", "empty"),
        ("test id", "space"),
        ("test@id", "special char"),
        ("test.id", "dot"),
        ("test/id", "slash"),
        ("test#id", "hash"),
    ])
    def test_validate_id_invalid(self, invalid_id, reason):
        """Test validate_id with invalid IDs."""
        with pytest.raises(ValidationError):
            InputValidator.validate_id(invalid_id)

    def test_validate_id_non_string(self):
        """Test validate_id with non-string input."""
        with pytest.raises(ValidationError, match="ID must be a string"):
            InputValidator.validate_id(123)

    def test_validate_id_custom_field_name(self):
        """Test validate_id with custom field name."""
        with pytest.raises(ValidationError, match="User ID cannot be empty"):
            InputValidator.validate_id("", "User ID")

    @pytest.mark.parametrize("valid_code", ["ja", "en", "fr", "de", "es"])
    def test_validate_language_code_valid(self, valid_code):
        """Test validate_language_code with valid codes."""
        result = InputValidator.validate_language_code(valid_code)
        assert result == valid_code

    @pytest.mark.parametrize("invalid_code,reason", [
        ("J", "too short"),
        ("JA", "uppercase"),
        ("eng", "too long"),
        ("j1", "contains number"),
        ("j-", "contains special char"),
        ("", "empty"),
    ])
    def test_validate_language_code_invalid(self, invalid_code, reason):
        """Test validate_language_code with invalid codes."""
        with pytest.raises(ValidationError):
            InputValidator.validate_language_code(invalid_code)

    def test_validate_language_code_non_string(self):
        """Test validate_language_code with non-string input."""
        with pytest.raises(ValidationError, match="Language code must be a string"):
            InputValidator.validate_language_code(123)

    def test_validate_url_valid(self):
        """Test validate_url with valid URLs."""
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "https://www.example.com",
            "https://example.com:8080",
            "https://example.com/path",
            "https://example.com/path?query=value",
            "http://localhost:3000",
            "https://192.168.1.1:8080"
        ]
        
        for url in valid_urls:
            result = InputValidator.validate_url(url)
            assert result == url

    def test_validate_url_invalid(self):
        """Test validate_url with invalid URLs."""
        invalid_urls = [
            "",  # empty
            "example.com",  # no protocol
            "ftp://example.com",  # wrong protocol
            "https://",  # incomplete
            "not-a-url",  # not a URL
        ]
        
        for invalid_url in invalid_urls:
            with pytest.raises(ValidationError):
                InputValidator.validate_url(invalid_url)

    def test_validate_url_non_string(self):
        """Test validate_url with non-string input."""
        with pytest.raises(ValidationError, match="URL must be a string"):
            InputValidator.validate_url(123)

    def test_validate_url_custom_field_name(self):
        """Test validate_url with custom field name."""
        with pytest.raises(ValidationError, match="API URL cannot be empty"):
            InputValidator.validate_url("", "API URL")

    def test_validate_path_valid(self):
        """Test validate_path with valid paths."""
        valid_paths = [
            "/",
            "/path/",
            "/path/to/resource/",
            "/api/v1/",
            "/123/",
        ]
        
        for path in valid_paths:
            result = InputValidator.validate_path(path)
            assert result == path

    def test_validate_path_invalid(self):
        """Test validate_path with invalid paths."""
        invalid_paths = [
            "",  # empty
            "path/",  # no leading slash
            "/path",  # no trailing slash
            "path",  # no slashes
        ]
        
        for invalid_path in invalid_paths:
            with pytest.raises(ValidationError):
                InputValidator.validate_path(invalid_path)

    def test_validate_path_non_string(self):
        """Test validate_path with non-string input."""
        with pytest.raises(ValidationError, match="Path must be a string"):
            InputValidator.validate_path(123)

    def test_validate_non_empty_string_valid(self):
        """Test validate_non_empty_string with valid strings."""
        valid_strings = [
            "test",
            "test string",
            "  test  ",  # whitespace is stripped internally
            "123",
        ]
        
        for string in valid_strings:
            result = InputValidator.validate_non_empty_string(string, "test_field")
            assert result == string

    def test_validate_non_empty_string_invalid(self):
        """Test validate_non_empty_string with invalid strings."""
        invalid_strings = [
            "",  # empty
            "   ",  # only whitespace
            "\t\n",  # only whitespace chars
        ]
        
        for invalid_string in invalid_strings:
            with pytest.raises(ValidationError, match="test_field cannot be empty"):
                InputValidator.validate_non_empty_string(invalid_string, "test_field")

    def test_validate_non_empty_string_non_string(self):
        """Test validate_non_empty_string with non-string input."""
        with pytest.raises(ValidationError, match="test_field must be a string"):
            InputValidator.validate_non_empty_string(123, "test_field")

    def test_validate_dict_valid(self):
        """Test validate_dict with valid dictionaries."""
        valid_dicts = [
            {},
            {"key": "value"},
            {"nested": {"key": "value"}},
        ]
        
        for valid_dict in valid_dicts:
            result = InputValidator.validate_dict(valid_dict, "test_dict")
            assert result == valid_dict

    def test_validate_dict_invalid(self):
        """Test validate_dict with invalid input."""
        invalid_inputs = [
            "string",
            123,
            [],
            None,
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValidationError, match="test_dict must be a dictionary"):
                InputValidator.validate_dict(invalid_input, "test_dict")

    def test_validate_list_valid(self):
        """Test validate_list with valid lists."""
        valid_lists = [
            [],
            ["item1", "item2"],
            [1, 2, 3],
            [{"key": "value"}],
        ]
        
        for valid_list in valid_lists:
            result = InputValidator.validate_list(valid_list, "test_list")
            assert result == valid_list

    def test_validate_list_invalid(self):
        """Test validate_list with invalid input."""
        invalid_inputs = [
            "string",
            123,
            {},
            None,
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValidationError, match="test_list must be a list"):
                InputValidator.validate_list(invalid_input, "test_list")

    def test_validate_optional_string_valid(self):
        """Test validate_optional_string with valid input."""
        valid_inputs = [
            None,
            "string",
            "",
            "  test  ",
        ]
        
        for valid_input in valid_inputs:
            result = InputValidator.validate_optional_string(valid_input, "test_field")
            assert result == valid_input

    def test_validate_optional_string_invalid(self):
        """Test validate_optional_string with invalid input."""
        invalid_inputs = [
            123,
            [],
            {},
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValidationError, match="test_field must be a string or None"):
                InputValidator.validate_optional_string(invalid_input, "test_field")

    def test_validate_enum_valid(self):
        """Test validate_enum with valid values."""
        valid_values = ["option1", "option2", "option3"]
        
        for value in valid_values:
            result = InputValidator.validate_enum(value, valid_values, "test_enum")
            assert result == value

    def test_validate_enum_invalid_value(self):
        """Test validate_enum with invalid value."""
        valid_values = ["option1", "option2", "option3"]
        
        with pytest.raises(ValidationError, match="test_enum must be one of"):
            InputValidator.validate_enum("invalid_option", valid_values, "test_enum")

    def test_validate_enum_non_string(self):
        """Test validate_enum with non-string input."""
        valid_values = ["option1", "option2", "option3"]
        
        with pytest.raises(ValidationError, match="test_enum must be a string"):
            InputValidator.validate_enum(123, valid_values, "test_enum")