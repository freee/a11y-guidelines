"""
Legacy compatibility module for YAML to JSON conversion.

This module provides backward compatibility by re-exporting functionality
that has been moved to more specialized modules (config.py and utils.py).
New code should use those modules directly instead.

@deprecated: Use config.py and utils.py modules instead
"""

from typing import Dict, Any

from . import config, utils

# Re-export constants for backward compatibility
LANGUAGES = utils.LANGUAGES
PICKLE_PATH = utils.PICKLE_PATH

# Re-export exception for backward compatibility
InitializerError = config.ConfigError

def setup_parameters() -> Dict[str, Any]:
    """
    @deprecated: Use config.setup_configuration() instead
    """
    return config.setup_configuration()

def get_info_links(basedir: str, baseurl: str = '') -> Dict[str, Any]:
    """
    @deprecated: Use utils.get_info_links() instead
    """
    return utils.get_info_links(basedir, baseurl)

def version_info(basedir: str) -> Dict[str, str]:
    """
    @deprecated: Use utils.get_version_info() instead
    """
    return utils.get_version_info(basedir)
