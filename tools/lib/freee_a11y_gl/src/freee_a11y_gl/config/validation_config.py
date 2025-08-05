"""Validation configuration management."""
from ..settings import settings


class ValidationConfig:
    """Manages validation configuration."""

    @classmethod
    def get_yaml_validation_mode(cls) -> str:
        """Get YAML validation mode.
        
        Returns:
            YAML validation mode ("strict", "warning", or "disabled")
        """
        return settings.get("validation.yaml_validation", "strict")

    @classmethod
    def set_yaml_validation_mode(cls, mode: str) -> None:
        """Set YAML validation mode.
        
        Args:
            mode: Validation mode ("strict", "warning", or "disabled")
            
        Raises:
            ValueError: If mode is not valid
        """
        valid_modes = ["strict", "warning", "disabled"]
        if mode not in valid_modes:
            raise ValueError(
                f"Invalid validation mode: {mode}. "
                f"Must be one of {valid_modes}")
        
        settings.set("validation.yaml_validation", mode)
