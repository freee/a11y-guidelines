"""Message and label configuration management."""
from typing import Optional
from ..settings import settings

LanguageCode = str  # Simplified type hint


class MessageConfig:
    """Manages message and label configuration."""

    @classmethod
    def get_check_tool_name(cls, tool_id: str,
                            lang: Optional[LanguageCode] = None) -> str:
        """Get localized check tool name."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_check_tool(tool_id, effective_lang)

    @classmethod
    def get_check_target_name(cls, target: str,
                              lang: Optional[LanguageCode] = None) -> str:
        """Get localized check target name."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_check_target(
            target, effective_lang)

    @classmethod
    def get_severity_tag(cls, severity: str,
                         lang: Optional[LanguageCode] = None) -> str:
        """Get localized severity tag."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_severity_tag(
            severity, effective_lang)

    @classmethod
    def get_platform_name(cls, platform: str,
                          lang: Optional[LanguageCode] = None) -> str:
        """Get localized platform name."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_platform_name(
            platform, effective_lang)

    @classmethod
    def get_implementation_target_name(cls, target: str,
                                       lang: Optional[LanguageCode] = None) -> str:
        """Get localized implementation target name."""
        effective_lang = (lang if lang is not None else
                          settings.get("languages.default", "ja"))
        return settings.message_catalog.get_implementation_target(
            target, effective_lang)
