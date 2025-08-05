"""Validation configuration management."""
from ..settings import settings
from ..exceptions import ConfigurationError
from ..validation_utils import InputValidator
from ..logging_config import get_logger

logger = get_logger()


class ValidationConfig:
    """Manages validation configuration."""

    @classmethod
    def get_yaml_validation_mode(cls) -> str:
        """Get YAML validation mode.
        
        Returns:
            YAML validation mode ("strict", "warning", or "disabled")
        """
        try:
            return settings.get("validation.yaml_validation", "strict")
        except Exception as e:
            logger.warning(f"Failed to get YAML validation mode: {e}")
            return "strict"

    @classmethod
    def set_yaml_validation_mode(cls, mode: str) -> None:
        """Set YAML validation mode.
        
        Args:
            mode: Validation mode ("strict", "warning", or "disabled")
            
        Raises:
            ConfigurationError: If mode is not valid
        """
        # Validate input
        mode = InputValidator.validate_non_empty_string(mode, "validation mode")
        mode = InputValidator.validate_enum(
            mode, ["strict", "warning", "disabled"], "validation mode"
        )
        
        try:
            settings.set("validation.yaml_validation", mode)
            logger.info(f"Set YAML validation mode to: {mode}")
        except Exception as e:
            raise ConfigurationError(
                f"Failed to set YAML validation mode to {mode}",
                str(e)
            )
