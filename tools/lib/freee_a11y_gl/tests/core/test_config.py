import pytest
from unittest.mock import patch, MagicMock
from freee_a11y_gl.config import Config
from freee_a11y_gl.settings import settings, Settings
from freee_a11y_gl.message_catalog import MessageCatalog

# Test data for mocking valid configuration
MOCK_CONFIG_DATA = {
    "check_tools": {
        "names": {
            "axe": {"ja": "axe-core", "en": "axe-core"},
            "lighthouse": {"ja": "Lighthouse", "en": "Lighthouse"},
            "wave": {"ja": "WAVE", "en": "WAVE"}
        }
    },
    "check_targets": {
        "names": {
            "design": {"ja": "デザイン", "en": "Design"},
            "code": {"ja": "コード", "en": "Code"},
            "product": {"ja": "プロダクト", "en": "Product"}
        }
    },
    "severity_tags": {
        "tags": {
            "minor": {"ja": "[軽微]", "en": "[MINOR]"},
            "normal": {"ja": "[通常]", "en": "[NORMAL]"},
            "major": {"ja": "[重要]", "en": "[MAJOR]"},
            "critical": {"ja": "[致命的]", "en": "[CRITICAL]"}
        }
    },
    "platform": {
        "names": {
            "web": {"ja": "Web", "en": "Web"},
            "mobile": {"ja": "モバイル", "en": "Mobile"},
            "general": {"ja": "全般", "en": "General"},
            "ios": {"ja": "iOS", "en": "iOS"},
            "android": {"ja": "Android", "en": "Android"}
        }
    }
}


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
        test_url = "https://example.com"
        Config.set_base_url(f"{test_url}/")
        assert settings.get("base_url") == test_url

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

    def test_get_platform_name_ja(self):
        """Test getting platform name for Japanese."""
        result = Config.get_platform_name("web", "ja")
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
        Config.get_examples_url(None)
        Config.get_date_format(None)


class TestConfigWithValidData:
    """Test cases for Config class with valid configuration data."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    def _create_mock_config(self):
        """Create a mock config object with valid data."""
        mock_config = MagicMock()
        
        # Mock check_tools
        mock_config.check_tools.names = MOCK_CONFIG_DATA["check_tools"]["names"]
        
        # Mock check_targets - create proper mock objects with new structure
        check_targets_mock = MagicMock()
        check_targets_mock.ja = {k: v["ja"] for k, v in MOCK_CONFIG_DATA["check_targets"]["names"].items()}
        check_targets_mock.en = {k: v["en"] for k, v in MOCK_CONFIG_DATA["check_targets"]["names"].items()}
        mock_config.check_targets = check_targets_mock
        
        # Mock severity_tags - create proper mock objects with new structure
        severity_tags_mock = MagicMock()
        severity_tags_mock.ja = {k: v["ja"] for k, v in MOCK_CONFIG_DATA["severity_tags"]["tags"].items()}
        severity_tags_mock.en = {k: v["en"] for k, v in MOCK_CONFIG_DATA["severity_tags"]["tags"].items()}
        mock_config.severity_tags = severity_tags_mock
        
        # Mock platform
        mock_config.platform.names = MOCK_CONFIG_DATA["platform"]["names"]
        
        return mock_config

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_with_valid_data_ja(self, mock_settings):
        """Test getting check tool name with valid data in Japanese."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the tool name
        mock_settings.message_catalog.get_check_tool.return_value = "axe-core"
        
        result = Config.get_check_tool_name("axe", "ja")
        assert result == "axe-core"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_with_valid_data_en(self, mock_settings):
        """Test getting check tool name with valid data in English."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "en"
        # Mock message catalog to return the tool name
        mock_settings.message_catalog.get_check_tool.return_value = "Lighthouse"
        
        result = Config.get_check_tool_name("lighthouse", "en")
        assert result == "Lighthouse"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_default_lang(self, mock_settings):
        """Test getting check tool name with default language."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the tool name
        mock_settings.message_catalog.get_check_tool.return_value = "WAVE"
        
        result = Config.get_check_tool_name("wave")
        assert result == "WAVE"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_with_valid_data_ja(self, mock_settings):
        """Test getting check target name with valid data in Japanese."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the target name
        mock_settings.message_catalog.get_check_target.return_value = "デザイン"
        
        result = Config.get_check_target_name("design", "ja")
        assert result == "デザイン"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_with_valid_data_en(self, mock_settings):
        """Test getting check target name with valid data in English."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "en"
        # Mock message catalog to return the target name
        mock_settings.message_catalog.get_check_target.return_value = "Code"
        
        result = Config.get_check_target_name("code", "en")
        assert result == "Code"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_default_lang(self, mock_settings):
        """Test getting check target name with default language."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the target name
        mock_settings.message_catalog.get_check_target.return_value = "プロダクト"
        
        result = Config.get_check_target_name("product")
        assert result == "プロダクト"

    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_with_valid_data_ja(self, mock_settings):
        """Test getting severity tag with valid data in Japanese."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the severity tag
        mock_settings.message_catalog.get_severity_tag.return_value = "[重要]"
        
        result = Config.get_severity_tag("major", "ja")
        assert result == "[重要]"

    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_with_valid_data_en(self, mock_settings):
        """Test getting severity tag with valid data in English."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "en"
        # Mock message catalog to return the severity tag
        mock_settings.message_catalog.get_severity_tag.return_value = "[CRITICAL]"
        
        result = Config.get_severity_tag("critical", "en")
        assert result == "[CRITICAL]"

    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_default_lang(self, mock_settings):
        """Test getting severity tag with default language."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the severity tag
        mock_settings.message_catalog.get_severity_tag.return_value = "[軽微]"
        
        result = Config.get_severity_tag("minor")
        assert result == "[軽微]"

    @pytest.mark.parametrize("target,lang,expected", [
        ("design", "ja", "デザイン"),
        ("design", "en", "Design"),
        ("code", "ja", "コード"),
        ("code", "en", "Code"),
        ("product", "ja", "プロダクト"),
        ("product", "en", "Product"),
    ])
    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_parametrized(self, mock_settings, target, lang, expected):
        """Test getting check target name with various combinations."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = lang
        # Mock message catalog to return the expected value
        mock_settings.message_catalog.get_check_target.return_value = expected
        
        result = Config.get_check_target_name(target, lang)
        assert result == expected

    @pytest.mark.parametrize("severity,lang,expected", [
        ("minor", "ja", "[軽微]"),
        ("minor", "en", "[MINOR]"),
        ("normal", "ja", "[通常]"),
        ("normal", "en", "[NORMAL]"),
        ("major", "ja", "[重要]"),
        ("major", "en", "[MAJOR]"),
        ("critical", "ja", "[致命的]"),
        ("critical", "en", "[CRITICAL]"),
    ])
    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_parametrized(self, mock_settings, severity, lang, expected):
        """Test getting severity tag with various combinations."""
        mock_settings.config = self._create_mock_config()
        mock_settings.get.return_value = lang
        # Mock message catalog to return the expected value
        mock_settings.message_catalog.get_severity_tag.return_value = expected
        
        result = Config.get_severity_tag(severity, lang)
        assert result == expected

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
        Config.get_examples_url(None)
        Config.get_date_format(None)


class TestConfigErrorHandling:
    """Test cases for Config class error handling."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_config_missing(self, mock_settings):
        """Test getting check tool name when config is missing."""
        mock_settings.config = MagicMock()
        mock_settings.config.check_tools = None
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_check_tool.return_value = "axe"
        
        result = Config.get_check_tool_name("axe")
        assert result == "axe"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_attribute_error(self, mock_settings):
        """Test getting check tool name when AttributeError occurs."""
        mock_settings.config = MagicMock()
        del mock_settings.config.check_tools  # This will cause AttributeError
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_check_tool.return_value = "axe"
        
        result = Config.get_check_tool_name("axe")
        assert result == "axe"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_tool_name_key_error(self, mock_settings):
        """Test getting check tool name when KeyError occurs."""
        mock_settings.config = MagicMock()
        mock_settings.config.check_tools.names = {}
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_check_tool.return_value = "nonexistent"
        
        result = Config.get_check_tool_name("nonexistent")
        assert result == "nonexistent"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_config_missing(self, mock_settings):
        """Test getting check target name when config is missing."""
        mock_settings.config = MagicMock()
        mock_settings.config.check_targets = None
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_check_target.return_value = "design"
        
        result = Config.get_check_target_name("design")
        assert result == "design"

    @patch('freee_a11y_gl.config.settings')
    def test_get_check_target_name_attribute_error(self, mock_settings):
        """Test getting check target name when AttributeError occurs."""
        mock_settings.config = MagicMock()
        del mock_settings.config.check_targets
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_check_target.return_value = "design"
        
        result = Config.get_check_target_name("design")
        assert result == "design"

    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_config_missing(self, mock_settings):
        """Test getting severity tag when config is missing."""
        mock_settings.config = MagicMock()
        mock_settings.config.severity_tags = None
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_severity_tag.return_value = "major"
        
        result = Config.get_severity_tag("major")
        assert result == "major"

    @patch('freee_a11y_gl.config.settings')
    def test_get_severity_tag_attribute_error(self, mock_settings):
        """Test getting severity tag when AttributeError occurs."""
        mock_settings.config = MagicMock()
        del mock_settings.config.severity_tags
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_severity_tag.return_value = "major"
        
        result = Config.get_severity_tag("major")
        assert result == "major"

    @patch('freee_a11y_gl.config.settings')
    def test_get_platform_name_config_missing(self, mock_settings):
        """Test getting platform name when config is missing."""
        mock_settings.config = MagicMock()
        mock_settings.config.platform = None
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_platform_name.return_value = "web"
        
        result = Config.get_platform_name("web")
        assert result == "web"

    @patch('freee_a11y_gl.config.settings')
    def test_get_platform_name_attribute_error(self, mock_settings):
        """Test getting platform name when AttributeError occurs."""
        mock_settings.config = MagicMock()
        del mock_settings.config.platform
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_platform_name.return_value = "web"
        
        result = Config.get_platform_name("web")
        assert result == "web"

    @patch('freee_a11y_gl.config.settings')
    def test_get_platform_name_lang_missing(self, mock_settings):
        """Test getting platform name when language is missing."""
        mock_settings.config = MagicMock()
        mock_settings.config.platform.names = {"en": {"web": "Web"}}  # Missing "ja"
        mock_settings.get.return_value = "ja"
        # Mock message catalog to return the original value (fallback behavior)
        mock_settings.message_catalog.get_platform_name.return_value = "web"
        
        result = Config.get_platform_name("web", "ja")
        assert result == "web"


class TestConfigInitialize:
    """Test cases for Config.initialize method."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    def test_initialize_with_profile(self):
        """Test initializing with a profile."""
        Config.initialize(profile="yaml2rst")
        # Profile should be set (we can't easily test this without mocking file system)
        # But we can test that it doesn't crash
        assert True

    def test_initialize_with_config_override(self):
        """Test initializing with config override."""
        Config.initialize(config_override={"base_url": "https://custom.example.com"})
        assert settings.get("base_url") == "https://custom.example.com"

    def test_initialize_with_both(self):
        """Test initializing with both profile and config override."""
        Config.initialize(
            profile="custom",
            config_override={"base_url": "https://custom.example.com"}
        )
        assert settings.get("base_url") == "https://custom.example.com"

    def test_initialize_none_values(self):
        """Test initializing with None values."""
        Config.initialize(profile=None, config_override=None)
        # Should not crash
        assert True


class TestMessageCatalog:
    """Test cases for MessageCatalog functionality."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    def test_message_catalog_property(self):
        """Test accessing message catalog property."""
        catalog = settings.message_catalog
        assert isinstance(catalog, MessageCatalog)

    def test_get_severity_tag_from_catalog(self):
        """Test getting severity tag from message catalog."""
        result = Config.get_severity_tag("major", "ja")
        assert result == "[MAJOR]"

    def test_get_check_target_from_catalog(self):
        """Test getting check target from message catalog."""
        result = Config.get_check_target_name("design", "ja")
        assert result == "デザイン"

    def test_get_check_tool_from_catalog(self):
        """Test getting check tool from message catalog."""
        result = Config.get_check_tool_name("axe", "ja")
        assert result == "axe-core"

    def test_get_platform_name_from_catalog(self):
        """Test getting platform name from message catalog."""
        result = Config.get_platform_name("mobile", "ja")
        assert result == "モバイル"

    def test_message_catalog_fallback(self):
        """Test message catalog fallback behavior."""
        # Test with non-existent values
        result = Config.get_severity_tag("nonexistent", "ja")
        assert result == "nonexistent"

    @patch('freee_a11y_gl.config.settings')
    def test_message_catalog_with_mock(self, mock_settings):
        """Test message catalog integration with mocked settings."""
        # Create a mock message catalog
        mock_catalog = MagicMock()
        mock_catalog.get_severity_tag.return_value = "[カスタム重要]"
        mock_settings.message_catalog = mock_catalog
        mock_settings.get.return_value = "ja"
        
        result = Config.get_severity_tag("major", "ja")
        assert result == "[カスタム重要]"
        mock_catalog.get_severity_tag.assert_called_once_with("major", "ja")


class TestConfigBackwardCompatibility:
    """Test cases for backward compatibility."""

    def setup_method(self):
        """Setup for each test method."""
        # Reset settings to a clean state by creating a new Settings instance
        settings.__dict__.clear()
        settings.__init__()

    def test_register_settings_still_works(self):
        """Test that register_settings still works for backward compatibility."""
        Config.register_settings({"base_url": "https://legacy.example.com"})
        assert settings.get("base_url") == "https://legacy.example.com"

    def test_all_existing_methods_work(self):
        """Test that all existing methods still work."""
        # This is a comprehensive test to ensure no breaking changes
        methods_to_test = [
            lambda: Config.get_base_url(),
            lambda: Config.get_guidelines_path(),
            lambda: Config.get_text_separator(),
            lambda: Config.get_list_separator(),
            lambda: Config.get_pass_singular_text(),
            lambda: Config.get_pass_plural_text(),
            lambda: Config.get_conjunction(),
            lambda: Config.get_check_tool_name("axe"),
            lambda: Config.get_check_target_name("design"),
            lambda: Config.get_severity_tag("major"),
            lambda: Config.get_platform_name("web"),
            lambda: Config.get_faq_path(),
            lambda: Config.get_examples_url(),
            lambda: Config.get_date_format(),
        ]
        
        for method in methods_to_test:
            try:
                result = method()
                # Just ensure it returns something and doesn't crash
                assert result is not None
            except Exception as e:
                pytest.fail(f"Method {method} failed with: {e}")
