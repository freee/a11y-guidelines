"""Configuration interface for freee_a11y_gl module."""
import re
from typing import Dict, Literal, Optional
from .settings import settings

LanguageCode = Literal["ja", "en"]

class Config:
    """Configuration interface."""

    @classmethod
    def register_settings(cls, new_settings: Optional[Dict[str, any]] = None) -> None:
        """Register new settings."""
        settings.update(new_settings)

    @classmethod
    def get_basedir(cls) -> str:
        """Get base directory path.
        
        Returns:
            Base directory path from settings, or '.' if not set
        """
        return settings.get("basedir", ".")

    @classmethod
    def get_base_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get base URL for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"urls.base.{effective_lang}", "")

    @classmethod
    def get_doc_path(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get documentation path for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"urls.docs.{effective_lang}", "/")

    @classmethod
    def get_separator(cls, lang: Optional[LanguageCode] = None, separator_type: Optional[str] = None) -> str:
        """Get separator of specified type for language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        effective_type = separator_type if separator_type is not None else "text"
        return settings.get(f"separators.{effective_type}.{effective_lang}", "")

    @classmethod
    def get_text_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get text separator for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"separators.text.{effective_lang}", "")

    @classmethod
    def get_list_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get list item separator for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"separators.list.{effective_lang}", ", ")

    @classmethod
    def get_pass_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Localized pass text
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"separators.pass_text.{effective_lang}", " is true")

    def get_conjunction(cls, lang: Optional[LanguageCode] = None, conjunction_type: Optional[str] = None) -> str:
        """Get conjunction of specified type for language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        effective_type = conjunction_type if conjunction_type is not None else "and"
        return settings.get(f"separators.{effective_type}_conjunction.{effective_lang}", " and ")

    @classmethod
    def get_check_tool_name(cls, tool_id: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized check tool name."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.check_tools.names[tool_id][effective_lang]
        except (KeyError, AttributeError):
            return tool_id

    @classmethod
    def get_check_target_name(cls, target: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized check target name."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.check_targets.names[target][effective_lang]
        except (KeyError, AttributeError):
            return target

    @classmethod
    def get_severity_tag(cls, severity: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized severity tag."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.severity_tags.tags[severity][effective_lang]
        except (KeyError, AttributeError):
            return severity

    @classmethod
    def get_implementation_target_name(cls, target: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized implementation target name."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.implementation_targets.targets[target][effective_lang]
        except (KeyError, AttributeError):
            return target

    @classmethod
    def get_platform_name(cls, platform: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized platform name."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.platform.names[platform][effective_lang]
        except (KeyError, AttributeError):
            return platform

    @classmethod
    def get_platform_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get platform list separator for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        try:
            return settings.config.platform.separator[effective_lang]
        except (KeyError, AttributeError):
            return ", "

    @classmethod
    def get_faq_path(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get FAQ path for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Path string for FAQ articles
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"urls.faq.{effective_lang}", "/faq/articles/")

    @classmethod
    def get_examples_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get examples base URL for specified language."""
        """Get examples base URL for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            URL string for examples in the specified language
        """
        base_url = cls.get_base_url(lang)
        return f"{base_url}/checks/examples/"

    @staticmethod
    @classmethod
    def get_date_format(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized date format string.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Date format string in strftime format
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        default_format = "%Y年%-m月%-d日" if effective_lang == "ja" else "%B %-d, %Y"
        return settings.get(f"formats.date.{effective_lang}", default_format)

    @staticmethod
    def tag2sc(tag: str) -> str:
        """Convert axe-core tag to WCAG SC identifier.
        
        Args:
            tag: axe-core tag (e.g., 'wcag111')
            
        Returns:
            WCAG SC identifier (e.g., '1.1.1')
        """
        return re.sub(r'wcag(\d)(\d)(\d+)', r'\1.\2.\3', tag)
