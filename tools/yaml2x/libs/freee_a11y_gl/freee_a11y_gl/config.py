"""Configuration settings for freee_a11y_gl module."""
import re
from typing import Dict, TypedDict, Literal, Any

LanguageCode = Literal["ja", "en"]

class BaseUrlConfig(TypedDict):
    ja: str
    en: str

class LocalizedSeparatorConfig(TypedDict):
    ja: str
    en: str

class PlatformConfig(TypedDict):
    names: Dict[str, Dict[LanguageCode, str]]
    separator: LocalizedSeparatorConfig

class CheckToolsConfig(TypedDict):
    names: Dict[str, Dict[LanguageCode, str]]

class CheckTargetsConfig(TypedDict):
    names: Dict[str, Dict[LanguageCode, str]]

class SeverityTagsConfig(TypedDict):
    tags: Dict[str, Dict[LanguageCode, str]]

class ImplementationTargetsConfig(TypedDict):
    targets: Dict[str, Dict[LanguageCode, str]]

class AxeCoreConfig(TypedDict):
    submodule_name: str
    base_dir: str
    deque_url: str
    msg_ja_file: str
    pkg_file: str
    rules_dir: str
    locale_dir: str
    locale_ja_file: str

class Config:
    """Global configuration settings."""
    
    # Base URLs for different languages
    BASE_URLS: BaseUrlConfig = {
        "ja": "https://a11y-guidelines.freee.co.jp",
        "en": "https://a11y-guidelines.freee.co.jp/en"
    }

    # Common path components
    COMMON_PATHS = {
        "categories": "categories",
        "checks": "checks",
        "examples": "examples"
    }

    # Document paths
    DOC_PATHS: BaseUrlConfig = {
        "ja": f"/{COMMON_PATHS['categories']}/",
        "en": f"/en/{COMMON_PATHS['categories']}/"
    }

    # Language-specific separators
    SEPARATORS = {
        "ja": {
            "text": "：",
            "list": "、",
            "and": "と",
            "or": "または",
            "and_conjunction": "、かつ",
            "or_conjunction": "、または"
        },
        "en": {
            "text": ": ",
            "list": ", ",
            "and": " and ",
            "or": " or ",
            "and_conjunction": ", and ",
            "or_conjunction": ", or "
        }
    }

    # Separator characters for different languages
    TEXT_SEPARATORS: LocalizedSeparatorConfig = {
        lang: SEPARATORS[lang]["text"] for lang in ["ja", "en"]
    }

    # List item separators
    LIST_SEPARATORS: LocalizedSeparatorConfig = {
        lang: SEPARATORS[lang]["list"] for lang in ["ja", "en"]
    }

    # Check tools configuration
    CHECK_TOOLS: CheckToolsConfig = {
        "names": {
            "nvda": {"ja": "NVDA", "en": "NVDA"},
            "macos-vo": {"ja": "macOS VoiceOver", "en": "macOS VoiceOver"},
            "axe": {"ja": "axe DevTools", "en": "axe DevTools"},
            "ios-vo": {"ja": "iOS VoiceOver", "en": "iOS VoiceOver"},
            "android-tb": {"ja": "Android TalkBack", "en": "Android TalkBack"},
            "keyboard": {"ja": "キーボード操作", "en": "Keyboard"},
            "misc": {"ja": "その他の手段", "en": "Miscellaneous Methods"}
        }
    }

    # Check targets configuration
    CHECK_TARGETS: CheckTargetsConfig = {
        "names": {
            "design": {"ja": "デザイン", "en": "Design"},
            "code": {"ja": "コード", "en": "Code"},
            "product": {"ja": "プロダクト", "en": "Product"}
        }
    }

    # Platform configuration
    PLATFORM: PlatformConfig = {
        "names": {
            "general": {"ja": "Web、モバイル", "en": "Web, Mobile"},
            "web": {"ja": "Web", "en": "Web"},
            "mobile": {"ja": "モバイル", "en": "Mobile"},
            "ios": {"ja": "iOS", "en": "iOS"},
            "android": {"ja": "Android", "en": "Android"}
        },
        "separator": {
            "ja": "、",
            "en": ", "
        }
    }

    # Severity configuration
    SEVERITY_TAGS: SeverityTagsConfig = {
        "tags": {
            "critical": {"ja": "[CRITICAL]", "en": "[CRITICAL]"},
            "major": {"ja": "[MAJOR]", "en": "[MAJOR]"},
            "normal": {"ja": "[NORMAL]", "en": "[NORMAL]"},
            "minor": {"ja": "[MINOR]", "en": "[MINOR]"}
        }
    }

    # Implementation targets configuration
    IMPLEMENTATION_TARGETS: ImplementationTargetsConfig = {
        "targets": {
            "web": {"ja": "Web", "en": "Web"},
            "android": {"ja": "Android", "en": "Android"},
            "ios": {"ja": "iOS", "en": "iOS"}
        }
    }

    # Axe Core configuration
    AXE_CORE: AxeCoreConfig = {
        "submodule_name": "vendor/axe-core",
        "base_dir": "vendor/axe-core",
        "deque_url": "https://dequeuniversity.com/rules/axe/",
        "msg_ja_file": "locales/ja.json",
        "pkg_file": "package.json",
        "rules_dir": "lib/rules",
        "locale_dir": "locales",
        "locale_ja_file": "ja.json"
    }

    # Example tool configuration - derive from BASE_URLS
    EXAMPLES_BASE_URLS: BaseUrlConfig = {
        "ja": f"{BASE_URLS['ja']}/{COMMON_PATHS['checks']}/{COMMON_PATHS['examples']}/",
        "en": f"{BASE_URLS['en']}/{COMMON_PATHS['checks']}/{COMMON_PATHS['examples']}/"
    }

    @classmethod
    def get_base_url(cls, lang: LanguageCode) -> str:
        """Get base URL for specified language.
        
        Args:
            lang: Language code
            
        Returns:
            Base URL string
        """
        return cls.BASE_URLS[lang]

    @classmethod
    def get_doc_path(cls, lang: LanguageCode) -> str:
        """Get documentation path for specified language.
        
        Args:
            lang: Language code
            
        Returns:
            Documentation path string
        """
        return cls.DOC_PATHS[lang]

    @classmethod
    def get_separator(cls, lang: LanguageCode, separator_type: str) -> str:
        """Get separator of specified type for language.
        
        Args:
            lang: Language code
            separator_type: Type of separator to get
            
        Returns:
            Separator string
        """
        return cls.SEPARATORS[lang][separator_type]

    @classmethod
    def get_text_separator(cls, lang: LanguageCode) -> str:
        """Get text separator for specified language."""
        return cls.get_separator(lang, "text")

    @classmethod
    def get_list_separator(cls, lang: LanguageCode) -> str:
        """Get list item separator for specified language."""
        return cls.get_separator(lang, "list")

    @classmethod
    def get_conjunction(cls, lang: LanguageCode, conjunction_type: str) -> str:
        """Get conjunction of specified type for language.
        
        Args:
            lang: Language code
            conjunction_type: Type of conjunction ('and' or 'or')
            
        Returns:
            Conjunction string
        """
        return cls.SEPARATORS[lang][f"{conjunction_type}_conjunction"]

    @classmethod
    def get_check_tool_name(cls, tool_id: str, lang: LanguageCode) -> str:
        """Get localized check tool name.
        
        Args:
            tool_id: Tool identifier
            lang: Language code
            
        Returns:
            Localized tool name
        """
        return cls.CHECK_TOOLS["names"][tool_id][lang]

    @classmethod
    def get_check_target_name(cls, target: str, lang: LanguageCode) -> str:
        """Get localized check target name.
        
        Args:
            target: Target identifier
            lang: Language code
            
        Returns:
            Localized target name
        """
        return cls.CHECK_TARGETS["names"][target][lang]

    @classmethod
    def get_severity_tag(cls, severity: str, lang: LanguageCode) -> str:
        """Get localized severity tag.
        
        Args:
            severity: Severity level
            lang: Language code
            
        Returns:
            Localized severity tag
        """
        return cls.SEVERITY_TAGS["tags"][severity][lang]

    @classmethod
    def get_implementation_target_name(cls, target: str, lang: LanguageCode) -> str:
        """Get localized implementation target name.
        
        Args:
            target: Target identifier
            lang: Language code
            
        Returns:
            Localized target name
        """
        return cls.IMPLEMENTATION_TARGETS["targets"][target][lang]

    @classmethod
    def get_platform_name(cls, platform: str, lang: LanguageCode) -> str:
        """Get localized platform name.
        
        Args:
            platform: Platform identifier
            lang: Language code
            
        Returns:
            Localized platform name
        """
        return cls.PLATFORM["names"][platform][lang]

    @classmethod
    def get_platform_separator(cls, lang: LanguageCode) -> str:
        """Get platform list separator for specified language.
        
        Args:
            lang: Language code
            
        Returns:
            Platform list separator string
        """
        return cls.PLATFORM["separator"][lang]

    @classmethod
    def get_examples_url(cls, lang: LanguageCode) -> str:
        """Get examples base URL for specified language.
        
        Args:
            lang: Language code
            
        Returns:
            Examples base URL string
        """
        return cls.EXAMPLES_BASE_URLS[lang]

    @staticmethod
    def tag2sc(tag: str) -> str:
        """Convert axe-core tag to WCAG SC identifier.
        
        Args:
            tag: axe-core tag (e.g., 'wcag111')
            
        Returns:
            WCAG SC identifier (e.g., '1.1.1')
        """
        return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
