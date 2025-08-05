"""External tool configuration management."""
from typing import Dict
from ..settings import settings


class ToolConfig:
    """Manages external tool configuration."""

    @classmethod
    def get_axe_core_config(cls) -> Dict[str, str]:
        """Get axe-core configuration.
        
        Returns:
            Dictionary containing axe-core configuration settings
        """
        return settings.get("axe_core", {})
