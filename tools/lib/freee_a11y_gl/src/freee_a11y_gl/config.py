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
    def set_base_url(cls, base_url: str) -> None:
        """Set the base URL for the site.
        
        Args:
            base_url: Base URL (e.g., https://a11y-guidelines.freee.co.jp)
        """
        settings.update({"base_url": base_url.rstrip("/")})

    @classmethod
    def get_basedir(cls) -> str:
        """Get base directory path.
        
        Returns:
            Base directory path from settings, or '.' if not set
        """
        return settings.get("basedir", ".")

    @classmethod
    def _get_language_path(cls, lang: LanguageCode) -> str:
        """Get the language-specific path segment.
        
        Args:
            lang: Language code
            
        Returns:
            Language path segment ("" for ja, "/en" for en)
        """
        return "" if lang == "ja" else f"/{lang}"

    @classmethod
    def get_base_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get base URL with language path for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Base URL with language path
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        base = settings.get("base_url", "")
        lang_path = cls._get_language_path(effective_lang)
        return f"{base}{lang_path}"

    @classmethod
    def get_guidelines_path(cls) -> str:
        """Get guidelines (categories) path."""
        return settings.get("paths.guidelines", "/categories/")

    @classmethod
    def get_separator(cls, lang: Optional[LanguageCode] = None, separator_type: Optional[str] = None) -> str:
        """Get separator of specified type for language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        effective_type = separator_type if separator_type is not None else "text"
        return settings.get(f"locale.{effective_lang}.{effective_type}_separator", "")

    @classmethod
    def get_text_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get text separator for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"locale.{effective_lang}.text_separator", "")

    @classmethod
    def get_list_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get list item separator for specified language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"locale.{effective_lang}.list_separator", ", ")

    @classmethod
    def get_pass_singular_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Localized pass text for single condition
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"locale.{effective_lang}.pass_singular_text", " is true")

    @classmethod
    def get_pass_plural_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Localized pass text for multiple conditions
        """
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        return settings.get(f"locale.{effective_lang}.pass_plural_text", " are true")

    @classmethod
    def get_conjunction(cls, lang: Optional[LanguageCode] = None, conjunction_type: Optional[str] = None) -> str:
        """Get conjunction of specified type for language."""
        effective_lang = lang if lang is not None else settings.get("languages.default", "ja")
        effective_type = conjunction_type if conjunction_type is not None else "and"
        return settings.get(f"locale.{effective_lang}.{effective_type}_conjunction", "and")

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
    def get_faq_path(cls) -> str:
        """Get FAQ path
        Returns:
            Path string for FAQ articles
        """
        return settings.get("paths.faq", "/faq/articles/")

    @classmethod
    def get_examples_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get examples base URL for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            URL string for examples in the specified language
        """
        base_url = cls.get_base_url(lang)
        return f"{base_url}/checks/examples/"

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
        return settings.get(f"locale.{effective_lang}.date_format", default_format)
