import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.config import Config
from freee_a11y_gl.settings import settings, Settings


class TestConfig:
    """Test cases for Config class."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    def test_register_settings(self):
        """Test registering new settings."""
        test_settings = {"test_key": "test_value"}
        Config.register_settings(test_settings)
        assert settings.get("test_key") == "test_value"

    def test_register_settings_none(self):
        """Test registering None settings does not crash."""
        Config.register_settings(None)

    def test_set_base_url(self):
        """Test setting base URL."""
        test_url = "https://example.com"
        Config.set_base_url(test_url)
        assert settings.get("base_url") == test_url

    def test_set_base_url_strips_trailing_slash(self):
        """Test that base URL trailing slash is stripped."""
        test_url = "https://example.com/"
        Config.set_base_url(test_url)
        assert settings.get("base_url") == "https://example.com"

    def test_get_basedir_default(self):
        """Test getting basedir with default value."""
        result = Config.get_basedir()
        assert result == "."

    def test_get_basedir_custom(self):
        """Test getting custom basedir."""
        settings.set("basedir", "/custom/path")
        result = Config.get_basedir()
        assert result == "/custom/path"

    def test_get_language_path_ja(self):
        """Test language path for Japanese."""
        result = Config._get_language_path("ja")
        assert result == ""

    def test_get_language_path_en(self):
        """Test language path for English."""
        result = Config._get_language_path("en")
        assert result == "/en"

    def test_get_base_url_default_lang(self):
        """Test getting base URL with default language."""
        settings.set("base_url", "https://example.com")
        result = Config.get_base_url()
        assert result == "https://example.com"

    def test_get_base_url_ja(self):
        """Test getting base URL for Japanese."""
        settings.set("base_url", "https://example.com")
        result = Config.get_base_url("ja")
        assert result == "https://example.com"

    def test_get_base_url_en(self):
        """Test getting base URL for English."""
        settings.set("base_url", "https://example.com")
        result = Config.get_base_url("en")
        assert result == "https://example.com/en"

    def test_get_guidelines_path(self):
        """Test getting guidelines path."""
        result = Config.get_guidelines_path()
        assert result == "/categories/"

    def test_get_guidelines_path_custom(self):
        """Test getting custom guidelines path."""
        settings.set("paths.guidelines", "/custom/guidelines/")
        result = Config.get_guidelines_path()
        assert result == "/custom/guidelines/"

    def test_get_separator_default(self):
        """Test getting separator with defaults."""
        result = Config.get_separator()
        assert result == "："

    def test_get_separator_custom_lang(self):
        """Test getting separator for specific language."""
        result = Config.get_separator("ja", "text")
        assert result == "："

    def test_get_text_separator_ja(self):
        """Test getting text separator for Japanese."""
        result = Config.get_text_separator("ja")
        assert result == "："

    def test_get_text_separator_en(self):
        """Test getting text separator for English."""
        result = Config.get_text_separator("en")
        assert result == ": "

    def test_get_list_separator_ja(self):
        """Test getting list separator for Japanese."""
        result = Config.get_list_separator("ja")
        assert result == "、"

    def test_get_list_separator_en(self):
        """Test getting list separator for English."""
        result = Config.get_list_separator("en")
        assert result == ", "

    def test_get_pass_singular_text_ja(self):
        """Test getting pass singular text for Japanese."""
        result = Config.get_pass_singular_text("ja")
        assert result == "を満たしている"

    def test_get_pass_singular_text_en(self):
        """Test getting pass singular text for English."""
        result = Config.get_pass_singular_text("en")
        assert result == " is true"

    def test_get_pass_plural_text_ja(self):
        """Test getting pass plural text for Japanese."""
        result = Config.get_pass_plural_text("ja")
        assert result == "を満たしている"

    def test_get_pass_plural_text_en(self):
        """Test getting pass plural text for English."""
        result = Config.get_pass_plural_text("en")
        assert result == " are true"

    def test_get_conjunction_default(self):
        """Test getting conjunction with defaults."""
        result = Config.get_conjunction()
        assert result == "、かつ"

    def test_get_conjunction_custom(self):
        """Test getting custom conjunction."""
        result = Config.get_conjunction("en", "or")
        assert result == ", or "

    def test_get_check_tool_name_missing(self):
        """Test getting check tool name when missing."""
        result = Config.get_check_tool_name("nonexistent")
        assert result == "nonexistent"

    def test_get_check_target_name_missing(self):
        """Test getting check target name when missing."""
        result = Config.get_check_target_name("nonexistent")
        assert result == "nonexistent"

    def test_get_severity_tag_missing(self):
        """Test getting severity tag when missing."""
        result = Config.get_severity_tag("nonexistent")
        assert result == "nonexistent"

    def test_get_implementation_target_name_missing(self):
        """Test getting implementation target name when missing."""
        result = Config.get_implementation_target_name("nonexistent")
        assert result == "nonexistent"

    def test_get_platform_name_ja(self):
        """Test getting platform name for Japanese."""
        result = Config.get_platform_name("web", "ja")
        print(result)
        assert result == "Web"

    def test_get_platform_name_mobile_ja(self):
        """Test getting mobile platform name for Japanese."""
        result = Config.get_platform_name("mobile", "ja")
        assert result == "モバイル"

    def test_get_platform_name_en(self):
        """Test getting platform name for English."""
        result = Config.get_platform_name("web", "en")
        assert result == "Web"

    def test_get_platform_name_missing(self):
        """Test getting platform name when missing."""
        result = Config.get_platform_name("nonexistent")
        assert result == "nonexistent"

    def test_get_platform_separator_ja(self):
        """Test getting platform separator for Japanese."""
        result = Config.get_platform_separator("ja")
        assert result == ", "

    def test_get_platform_separator_en(self):
        """Test getting platform separator for English."""
        result = Config.get_platform_separator("en")
        assert result == ", "

    def test_get_faq_path(self):
        """Test getting FAQ path."""
        result = Config.get_faq_path()
        assert result == "/faq/articles/"

    def test_get_faq_path_custom(self):
        """Test getting custom FAQ path."""
        settings.set("paths.faq", "/custom/faq/")
        result = Config.get_faq_path()
        assert result == "/custom/faq/"

    def test_get_examples_url_ja(self):
        """Test getting examples URL for Japanese."""
        settings.set("base_url", "https://example.com")
        result = Config.get_examples_url("ja")
        assert result == "https://example.com/checks/examples/"

    def test_get_examples_url_en(self):
        """Test getting examples URL for English."""
        settings.set("base_url", "https://example.com")
        result = Config.get_examples_url("en")
        assert result == "https://example.com/en/checks/examples/"

    def test_get_date_format_ja(self):
        """Test getting date format for Japanese."""
        result = Config.get_date_format("ja")
        assert result == "%Y年%-m月%-d日"

    def test_get_date_format_en(self):
        """Test getting date format for English."""
        result = Config.get_date_format("en")
        assert result == "%B %-d, %Y"

    def test_get_date_format_default(self):
        """Test getting date format with default language."""
        result = Config.get_date_format()
        assert result == "%Y年%-m月%-d日"  # Default is ja

    def test_method_chaining_with_none_values(self):
        """Test that methods handle None values gracefully."""
        # These should not crash and should use defaults
        Config.get_base_url(None)
        Config.get_text_separator(None)
        Config.get_list_separator(None)
        Config.get_pass_singular_text(None)
        Config.get_pass_plural_text(None)
        Config.get_conjunction(None, None)
        Config.get_check_tool_name("test", None)
        Config.get_platform_name("web", None)
        Config.get_platform_separator(None)
        Config.get_examples_url(None)
        Config.get_date_format(None)