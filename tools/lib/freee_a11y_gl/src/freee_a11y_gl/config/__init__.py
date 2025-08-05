"""Configuration module for freee_a11y_gl."""
from .path_config import PathConfig
from .localization_config import LocalizationConfig
from .message_config import MessageConfig
from .validation_config import ValidationConfig
from .tool_config import ToolConfig

# Re-export the main Config class and types
from ..config_main import Config, LanguageCode
from ..settings import settings

__all__ = [
    "Config",
    "LanguageCode",
    "settings",
    "PathConfig",
    "LocalizationConfig",
    "MessageConfig",
    "ValidationConfig",
    "ToolConfig",
]
