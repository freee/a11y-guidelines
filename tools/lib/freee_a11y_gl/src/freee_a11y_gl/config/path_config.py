"""Path and URL configuration management."""
from typing import Optional
from ..settings import settings
from ..validation_utils import InputValidator
from ..logging_config import get_logger

logger = get_logger()

LanguageCode = str  # Simplified type hint


class PathConfig:
    """Manages path and URL configuration."""

    @classmethod
    def get_language_path(cls, lang: LanguageCode) -> str:
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
            lang: Language code. If None, default language from settings
                  will be used.

        Returns:
            Base URL with language path
        """
        # Validate inputs
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)

        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            base = settings.get("base_url", "")
            if base:
                InputValidator.validate_url(base, "base URL")
            lang_path = cls.get_language_path(effective_lang)
            return f"{base}{lang_path}"
        except Exception as e:
            logger.warning(f"Failed to get base URL: {e}")
            return ""  # Fallback to empty string

    @classmethod
    def get_guidelines_path(cls) -> str:
        """Get guidelines (categories) path."""
        return settings.get("paths.guidelines", "/categories/")

    @classmethod
    def get_faq_path(cls) -> str:
        """Get FAQ path.

        Returns:
            Path string for FAQ articles
        """
        return settings.get("paths.faq", "/faq/articles/")

    @classmethod
    def get_examples_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get examples base URL for specified language.

        Args:
            lang: Language code. If None, default language from settings
                  will be used.

        Returns:
            URL string for examples in the specified language
        """
        # Validate inputs
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)

        try:
            base_url = cls.get_base_url(lang)
            return f"{base_url}/checks/examples/"
        except Exception as e:
            logger.warning(f"Failed to get examples URL: {e}")
            return "/checks/examples/"  # Fallback to relative path
