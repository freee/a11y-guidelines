"""Localization configuration management."""
from typing import List, Optional
from ..settings import settings

LanguageCode = str  # Simplified type hint


class LocalizationConfig:
    """Manages localization-related configuration."""

    @classmethod
    def get_separator(cls, lang: Optional[LanguageCode] = None,
                      separator_type: Optional[str] = None) -> str:
        """Get separator of specified type for language."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        effective_type = (separator_type if separator_type is not None
                          else "text")
        return settings.message_catalog.get_separator(effective_type, effective_lang)

    @classmethod
    def get_text_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get text separator for specified language."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_separator(
            "text", effective_lang)

    @classmethod
    def get_list_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get list item separator for specified language."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_separator(
            "list", effective_lang)

    @classmethod
    def get_pass_singular_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings
                  will be used.
            
        Returns:
            Localized pass text for single condition
        """
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_pass_text(
            "singular", effective_lang)

    @classmethod
    def get_pass_plural_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings
                  will be used.
            
        Returns:
            Localized pass text for multiple conditions
        """
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_pass_text(
            "plural", effective_lang)

    @classmethod
    def get_conjunction(cls, lang: Optional[LanguageCode] = None,
                        conjunction_type: Optional[str] = None) -> str:
        """Get conjunction of specified type for language."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        effective_type = (conjunction_type if conjunction_type is not None
                          else "and")
        return settings.message_catalog.get_conjunction(
            effective_type, effective_lang)

    @classmethod
    def get_date_format(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized date format string.
        
        Args:
            lang: Language code. If None, default language from settings
                  will be used.
            
        Returns:
            Date format string in strftime format
        """
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_date_format(
            "default", effective_lang)

    @classmethod
    def get_available_languages(cls) -> List[str]:
        """Get list of available languages.
        
        Returns:
            List of available language codes
        """
        return settings.get("languages.available", ["ja", "en"])

    @classmethod
    def get_default_language(cls) -> str:
        """Get default language code.
        
        Returns:
            Default language code
        """
        return settings.get("languages.default", "ja")
