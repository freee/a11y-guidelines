"""Message and label configuration management."""
from typing import Optional
from ..settings import settings
from ..exceptions import MessageCatalogError
from ..validation_utils import InputValidator
from ..logging_config import get_logger

logger = get_logger()

LanguageCode = str  # Simplified type hint


class MessageConfig:
    """Manages message and label configuration."""

    @classmethod
    def get_check_tool_name(cls, tool_id: str,
                            lang: Optional[LanguageCode] = None) -> str:
        """Get localized check tool name."""
        # Validate inputs
        tool_id = InputValidator.validate_non_empty_string(tool_id, "tool_id")
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)
        
        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            return settings.message_catalog.get_check_tool(tool_id, effective_lang)
        except Exception as e:
            logger.warning(f"Failed to get check tool name for {tool_id}: {e}")
            return tool_id  # Fallback to original ID

    @classmethod
    def get_check_target_name(cls, target: str,
                              lang: Optional[LanguageCode] = None) -> str:
        """Get localized check target name."""
        # Validate inputs
        target = InputValidator.validate_non_empty_string(target, "target")
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)
        
        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            return settings.message_catalog.get_check_target(
                target, effective_lang)
        except Exception as e:
            logger.warning(f"Failed to get check target name for {target}: {e}")
            return target  # Fallback to original target

    @classmethod
    def get_severity_tag(cls, severity: str,
                         lang: Optional[LanguageCode] = None) -> str:
        """Get localized severity tag."""
        # Validate inputs
        severity = InputValidator.validate_non_empty_string(severity, "severity")
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)
        
        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            return settings.message_catalog.get_severity_tag(
                severity, effective_lang)
        except Exception as e:
            logger.warning(f"Failed to get severity tag for {severity}: {e}")
            return severity  # Fallback to original severity

    @classmethod
    def get_platform_name(cls, platform: str,
                          lang: Optional[LanguageCode] = None) -> str:
        """Get localized platform name."""
        # Validate inputs
        platform = InputValidator.validate_non_empty_string(platform, "platform")
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)
        
        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            return settings.message_catalog.get_platform_name(
                platform, effective_lang)
        except Exception as e:
            logger.warning(f"Failed to get platform name for {platform}: {e}")
            return platform  # Fallback to original platform

    @classmethod
    def get_implementation_target_name(cls, target: str,
                                       lang: Optional[LanguageCode] = None) -> str:
        """Get localized implementation target name."""
        # Validate inputs
        target = InputValidator.validate_non_empty_string(target, "target")
        if lang is not None:
            lang = InputValidator.validate_language_code(lang)
        
        try:
            effective_lang = (lang if lang is not None else
                              settings.get("languages.default", "ja"))
            return settings.message_catalog.get_implementation_target(
                target, effective_lang)
        except Exception as e:
            logger.warning(f"Failed to get implementation target name for {target}: {e}")
            return target  # Fallback to original target
