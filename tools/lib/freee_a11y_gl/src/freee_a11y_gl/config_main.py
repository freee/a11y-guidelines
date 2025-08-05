"""Configuration interface for freee_a11y_gl module."""
from typing import Any, Dict, List, Literal, Optional
from .settings import settings
from .exceptions import ConfigurationError
from .validation_utils import InputValidator
from .logging_config import get_logger

logger = get_logger()
from .config.path_config import PathConfig
from .config.localization_config import LocalizationConfig
from .config.message_config import MessageConfig
from .config.validation_config import ValidationConfig
from .config.tool_config import ToolConfig

LanguageCode = Literal["ja", "en"]


class Config:
    """Configuration interface."""

    @classmethod
    def initialize(cls, profile: Optional[str] = None, config_override: Optional[Dict[str, Any]] = None) -> None:
        """Initialize configuration with profile and overrides.
        
        This method allows you to initialize the library's configuration with a specific
        profile and optional configuration overrides. This is the recommended way to
        configure the library for different use cases.
        
        Args:
            profile: Profile name to use (e.g., "yaml2rst", "yaml2sheet", "custom_project").
                    If None, uses "default" profile.
            config_override: Dictionary of settings to override. Can contain nested
                           dictionaries for hierarchical configuration.
                           
        Examples:
            # Use a specific profile
            Config.initialize(profile="yaml2rst")
            
            # Use profile with custom overrides
            Config.initialize(
                profile="yaml2sheet",
                config_override={
                    "base_url": "https://custom.example.com",
                    "basedir": "/path/to/project",
                    "languages": {
                        "default": "en"
                    },
                    "paths": {
                        "guidelines": "/custom/categories/"
                    }
                }
            )
            
        Note:
            This method should be called before using other Config methods.
            Settings are validated after initialization. Localized strings should
            be configured through message catalog files, not through config_override.
        """
        settings.initialize(profile=profile, config_override=config_override)

    @classmethod
    def register_settings(cls, new_settings: Optional[Dict[str, Any]] = None) -> None:
        """Register new settings with validation.
        
        This method allows you to customize the library's configuration by providing
        a dictionary of settings that will be merged with the existing configuration.
        
        Args:
            new_settings: Dictionary of settings to register. Can contain nested
                         dictionaries for hierarchical configuration.
                         
        Examples:
            # Simple configuration
            Config.register_settings({
                "base_url": "https://custom.example.com"
            })
            
            # Complex nested configuration
            Config.register_settings({
                "base_url": "https://custom.example.com",
                "basedir": "/path/to/project",
                "languages": {
                    "default": "en",
                    "available": ["ja", "en"]
                },
                "paths": {
                    "guidelines": "/custom/categories/",
                    "faq": "/custom/faq/"
                }
            })
            
        Note:
            Settings are validated after registration. Invalid configurations
            will raise a validation error. Localized strings should be configured
            through message catalog files, not through this method.
        """
        settings.update(new_settings)

    @classmethod
    def set_base_url(cls, base_url: str) -> None:
        """Set the base URL for the site.
        
        Args:
            base_url: Base URL (e.g., https://a11y-guidelines.freee.co.jp)
            
        Raises:
            ConfigurationError: If base_url is invalid
        """
        # Validate input
        base_url = InputValidator.validate_url(base_url, "base URL")
        
        try:
            settings.update({"base_url": base_url.rstrip("/")})
            logger.info(f"Set base URL to: {base_url}")
        except Exception as e:
            raise ConfigurationError(
                f"Failed to set base URL to {base_url}",
                str(e)
            )

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
        return PathConfig.get_language_path(lang)

    @classmethod
    def get_base_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get base URL with language path for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Base URL with language path
        """
        return PathConfig.get_base_url(lang)

    @classmethod
    def get_guidelines_path(cls) -> str:
        """Get guidelines (categories) path."""
        return PathConfig.get_guidelines_path()

    @classmethod
    def get_separator(cls, lang: Optional[LanguageCode] = None, separator_type: Optional[str] = None) -> str:
        """Get separator of specified type for language."""
        return LocalizationConfig.get_separator(lang, separator_type)

    @classmethod
    def get_text_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get text separator for specified language."""
        return LocalizationConfig.get_text_separator(lang)

    @classmethod
    def get_list_separator(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get list item separator for specified language."""
        return LocalizationConfig.get_list_separator(lang)

    @classmethod
    def get_pass_singular_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Localized pass text for single condition
        """
        return LocalizationConfig.get_pass_singular_text(lang)

    @classmethod
    def get_pass_plural_text(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized pass text for conditions.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Localized pass text for multiple conditions
        """
        return LocalizationConfig.get_pass_plural_text(lang)

    @classmethod
    def get_conjunction(cls, lang: Optional[LanguageCode] = None, conjunction_type: Optional[str] = None) -> str:
        """Get conjunction of specified type for language."""
        return LocalizationConfig.get_conjunction(lang, conjunction_type)

    @classmethod
    def get_check_tool_name(cls, tool_id: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized check tool name."""
        return MessageConfig.get_check_tool_name(tool_id, lang)

    @classmethod
    def get_check_target_name(cls, target: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized check target name."""
        return MessageConfig.get_check_target_name(target, lang)

    @classmethod
    def get_severity_tag(cls, severity: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized severity tag."""
        return MessageConfig.get_severity_tag(severity, lang)

    @classmethod
    def get_platform_name(cls, platform: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized platform name."""
        return MessageConfig.get_platform_name(platform, lang)

    @classmethod
    def get_implementation_target_name(cls, target: str, lang: Optional[LanguageCode] = None) -> str:
        """Get localized implementation target name."""
        return MessageConfig.get_implementation_target_name(target, lang)

    @classmethod
    def get_faq_path(cls) -> str:
        """Get FAQ path
        Returns:
            Path string for FAQ articles
        """
        return PathConfig.get_faq_path()

    @classmethod
    def get_examples_url(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get examples base URL for specified language.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            URL string for examples in the specified language
        """
        return PathConfig.get_examples_url(lang)

    @classmethod
    def get_date_format(cls, lang: Optional[LanguageCode] = None) -> str:
        """Get localized date format string.
        
        Args:
            lang: Language code. If None, default language from settings will be used.
            
        Returns:
            Date format string in strftime format
        """
        return LocalizationConfig.get_date_format(lang)

    @classmethod
    def get_available_languages(cls) -> List[str]:
        """Get list of available languages.
        
        Returns:
            List of available language codes
        """
        return LocalizationConfig.get_available_languages()

    @classmethod
    def get_default_language(cls) -> str:
        """Get default language code.
        
        Returns:
            Default language code
        """
        return LocalizationConfig.get_default_language()

    @classmethod
    def get_yaml_validation_mode(cls) -> str:
        """Get YAML validation mode.
        
        Returns:
            YAML validation mode ("strict", "warning", or "disabled")
        """
        return ValidationConfig.get_yaml_validation_mode()

    @classmethod
    def set_yaml_validation_mode(cls, mode: str) -> None:
        """Set YAML validation mode.
        
        Args:
            mode: Validation mode ("strict", "warning", or "disabled")
            
        Raises:
            ValueError: If mode is not valid
        """
        return ValidationConfig.set_yaml_validation_mode(mode)

    @classmethod
    def get_axe_core_config(cls) -> Dict[str, str]:
        """Get axe-core configuration.
        
        Returns:
            Dictionary containing axe-core configuration settings
        """
        return ToolConfig.get_axe_core_config()
