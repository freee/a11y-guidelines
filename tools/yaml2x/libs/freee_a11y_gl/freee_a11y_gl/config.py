"""Configuration interface for freee_a11y_gl module."""
import re
from typing import Dict, Literal
from .settings import settings

LanguageCode = Literal["ja", "en"]

class Config:
    """Configuration interface."""

    @classmethod
    def register_settings(cls, new_settings: Dict[str, any]) -> None:
        """Register new settings."""
        settings.update(new_settings)

    @classmethod
    def get_base_url(cls, lang: LanguageCode) -> str:
        """Get base URL for specified language."""
        return settings.get(f"urls.base.{lang}")

    @classmethod
    def get_doc_path(cls, lang: LanguageCode) -> str:
        """Get documentation path for specified language."""
        return settings.get(f"urls.docs.{lang}")

    @classmethod
    def get_separator(cls, lang: LanguageCode, separator_type: str) -> str:
        """Get separator of specified type for language."""
        return settings.get(f"separators.{separator_type}.{lang}")

    @classmethod
    def get_text_separator(cls, lang: LanguageCode) -> str:
        """Get text separator for specified language."""
        return settings.get(f"separators.text.{lang}")

    @classmethod
    def get_list_separator(cls, lang: LanguageCode) -> str:
        """Get list item separator for specified language."""
        return settings.get(f"separators.list.{lang}")

    @classmethod
    def get_conjunction(cls, lang: LanguageCode, conjunction_type: str) -> str:
        """Get conjunction of specified type for language."""
        return settings.get(f"separators.{conjunction_type}_conjunction.{lang}")

    @classmethod
    def get_check_tool_name(cls, tool_id: str, lang: LanguageCode) -> str:
        """Get localized check tool name."""
        return settings.config.check_tools.names[tool_id][lang]

    @classmethod
    def get_check_target_name(cls, target: str, lang: LanguageCode) -> str:
        """Get localized check target name."""
        return settings.config.check_targets.names[target][lang]

    @classmethod
    def get_severity_tag(cls, severity: str, lang: LanguageCode) -> str:
        """Get localized severity tag."""
        return settings.config.severity_tags.tags[severity][lang]

    @classmethod
    def get_implementation_target_name(cls, target: str, lang: LanguageCode) -> str:
        """Get localized implementation target name."""
        return settings.config.implementation_targets.targets[target][lang]

    @classmethod
    def get_platform_name(cls, platform: str, lang: LanguageCode) -> str:
        """Get localized platform name."""
        return settings.config.platform.names[platform][lang]

    @classmethod
    def get_platform_separator(cls, lang: LanguageCode) -> str:
        """Get platform list separator for specified language."""
        return settings.config.platform.separator[lang]

    @classmethod
    def get_examples_url(cls, lang: LanguageCode) -> str:
        """Get examples base URL for specified language."""
        base_url = cls.get_base_url(lang)
        return f"{base_url}/checks/examples/"

    @staticmethod
    def tag2sc(tag: str) -> str:
        """Convert axe-core tag to WCAG SC identifier.
        
        Args:
            tag: axe-core tag (e.g., 'wcag111')
            
        Returns:
            WCAG SC identifier (e.g., '1.1.1')
        """
        return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
