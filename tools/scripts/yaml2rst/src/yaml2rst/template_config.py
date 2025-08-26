"""Template configuration management for yaml2rst.

This module provides configuration management specifically for template
customization in yaml2rst. It handles loading configuration from files,
environment variables, and provides default values for template-related
settings.

The configuration system is independent of freee_a11y_gl and operates
entirely within the yaml2rst package scope.
"""
import os
import configparser
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging


class TemplateConfigError(Exception):
    """Base exception for template configuration errors."""
    pass


class TemplateConfig:
    """Manages template-related configuration for yaml2rst.

    This class provides a centralized way to manage template configuration,
    including user template directories, fallback behavior, and configuration
    file loading. It supports both configuration files and environment
    variable overrides.

    Configuration Sources (in order of precedence):
    1. Environment variables (YAML2RST_*)
    2. Configuration file (~/.config/freee_a11y_gl/yaml2rst.conf)
    3. Default values

    Example:
        >>> config = TemplateConfig()
        >>> user_dir = config.get_user_template_dir()
        >>> search_paths = config.get_template_search_paths()
    """

    # Default configuration values
    DEFAULT_USER_DIR = "~/.config/freee_a11y_gl/templates"
    DEFAULT_CONFIG_FILE = "~/.config/freee_a11y_gl/yaml2rst.conf"
    DEFAULT_FALLBACK_TO_BUILTIN = True

    # Environment variable names
    ENV_USER_TEMPLATE_DIR = "YAML2RST_USER_TEMPLATE_DIR"
    ENV_CONFIG_FILE = "YAML2RST_CONFIG_FILE"
    ENV_FALLBACK_TO_BUILTIN = "YAML2RST_FALLBACK_TO_BUILTIN"

    def __init__(self, config_file: Optional[str] = None):
        """Initialize template configuration.

        Args:
            config_file: Optional path to configuration file. If None,
                        uses default location or environment variable.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self._config_file = config_file
        self._config_cache: Optional[Dict[str, Any]] = None

        # Override attributes for testing/customization
        self.built_in_template_dir: Optional[Path] = None
        self.user_template_dir: Optional[Path] = None
        self.custom_template_dir: Optional[str] = None

    def get_config_file_path(self) -> Path:
        """Get the configuration file path.

        Returns:
            Path to the configuration file (may not exist)
        """
        if self._config_file:
            return Path(self._config_file).expanduser()

        # Check environment variable
        env_config = os.getenv(self.ENV_CONFIG_FILE)
        if env_config:
            return Path(env_config).expanduser()

        # Use default
        return Path(self.DEFAULT_CONFIG_FILE).expanduser()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from all sources.

        Loads configuration from file and applies environment variable
        overrides. Results are cached for subsequent calls.

        Returns:
            Dictionary containing all configuration values

        Raises:
            TemplateConfigError: If configuration file exists but is invalid
        """
        if self._config_cache is not None:
            return self._config_cache

        # Start with defaults
        config = {
            'user_template_dir': self.DEFAULT_USER_DIR,
            'fallback_to_builtin': self.DEFAULT_FALLBACK_TO_BUILTIN
        }

        # Load from configuration file
        config_file_path = self.get_config_file_path()
        if config_file_path.exists():
            try:
                file_config = self._load_config_file(config_file_path)
                config.update(file_config)
                self.logger.debug(
                    f"Loaded configuration from {config_file_path}"
                )
            except Exception as e:
                raise TemplateConfigError(
                    f"Failed to load configuration file "
                    f"{config_file_path}: {e}"
                ) from e

        # Apply environment variable overrides
        env_overrides = self._load_env_overrides()
        config.update(env_overrides)

        # Cache the result
        self._config_cache = config
        return config

    def _load_config_file(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from a file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dictionary containing configuration from file

        Raises:
            TemplateConfigError: If file format is invalid
        """
        parser = configparser.ConfigParser()

        try:
            parser.read(config_path)
        except configparser.Error as e:
            raise TemplateConfigError(
                f"Invalid configuration file format: {e}"
            ) from e

        config = {}

        if 'templates' in parser:
            templates_section = parser['templates']

            # Load string values
            if 'user_template_dir' in templates_section:
                config['user_template_dir'] = (
                    templates_section['user_template_dir'])

            # Load boolean values
            if 'fallback_to_builtin' in templates_section:
                try:
                    config['fallback_to_builtin'] = (
                        templates_section.getboolean('fallback_to_builtin'))
                except ValueError as e:
                    raise TemplateConfigError(
                        f"Invalid boolean value for "
                        f"fallback_to_builtin: {e}"
                    ) from e

        return config

    def _load_env_overrides(self) -> Dict[str, Any]:
        """Load configuration overrides from environment variables.

        Returns:
            Dictionary containing environment variable overrides
        """
        overrides = {}

        # String values
        if os.getenv(self.ENV_USER_TEMPLATE_DIR):
            overrides['user_template_dir'] = os.getenv(
                self.ENV_USER_TEMPLATE_DIR)

        # Boolean values
        if os.getenv(self.ENV_FALLBACK_TO_BUILTIN):
            env_value = os.getenv(self.ENV_FALLBACK_TO_BUILTIN, '').lower()
            if env_value in ('true', '1', 'yes', 'on'):
                overrides['fallback_to_builtin'] = True
            elif env_value in ('false', '0', 'no', 'off'):
                overrides['fallback_to_builtin'] = False
            else:
                self.logger.warning(
                    f"Invalid boolean value for "
                    f"{self.ENV_FALLBACK_TO_BUILTIN}: {env_value}. "
                    f"Using default."
                )

        if overrides:
            self.logger.debug(
                f"Applied environment overrides: {overrides}")

        return overrides

    def get_user_template_dir(self) -> str:
        """Get the user template directory path.

        Returns:
            Path to user template directory (may not exist)
        """
        config = self.load_config()
        return config['user_template_dir']

    def get_user_template_dir_expanded(self) -> Path:
        """Get the user template directory as an expanded Path object.

        Returns:
            Expanded Path object for user template directory
        """
        return Path(self.get_user_template_dir()).expanduser()

    def should_fallback_to_builtin(self) -> bool:
        """Check if fallback to builtin templates is enabled.

        Returns:
            True if fallback to builtin templates is enabled
        """
        config = self.load_config()
        return config['fallback_to_builtin']

    def get_template_search_paths(
            self, custom_dir: Optional[str] = None) -> List[str]:
        """Get template search paths in priority order.

        Args:
            custom_dir: Optional custom template directory (highest priority)

        Returns:
            List of template directory paths in search order
        """
        paths = []

        # 1. Custom directory (highest priority)
        # Use override attribute if set, otherwise use parameter
        effective_custom_dir = custom_dir or self.custom_template_dir
        if effective_custom_dir:
            paths.append(str(Path(effective_custom_dir).expanduser()))

        # 2. User template directory
        # Use override attribute if set, otherwise use config
        if self.user_template_dir:
            paths.append(str(self.user_template_dir))
        else:
            user_dir = self.get_user_template_dir_expanded()
            if user_dir.exists():
                paths.append(str(user_dir))

        # 3. Builtin templates (fallback)
        if self.should_fallback_to_builtin():
            if self.built_in_template_dir:
                paths.append(str(self.built_in_template_dir))
            else:
                from .path import TEMPLATE_DIR
                paths.append(TEMPLATE_DIR)

        return paths

    def clear_cache(self) -> None:
        """Clear the configuration cache.

        This forces the next call to load_config() to reload from sources.
        Useful for testing or when configuration files change at runtime.
        """
        self._config_cache = None

    def validate_config(self) -> List[str]:
        """Validate the current configuration.

        Returns:
            List of validation warnings (empty if all valid)
        """
        warnings = []
        config = self.load_config()

        # Check if user template directory is accessible
        user_dir = Path(config['user_template_dir']).expanduser()
        if user_dir.exists() and not user_dir.is_dir():
            warnings.append(
                f"User template path exists but is not a directory: {user_dir}"
            )

        # Check if we have at least one valid template source
        search_paths = self.get_template_search_paths()
        valid_paths = [p for p in search_paths if Path(p).exists()]
        if not valid_paths:
            warnings.append("No valid template directories found")

        return warnings
