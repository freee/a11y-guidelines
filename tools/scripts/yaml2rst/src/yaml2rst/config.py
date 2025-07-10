# Language configuration is now managed by freee_a11y_gl library
# Import available languages from the library configuration
from freee_a11y_gl.config import Config

def get_available_languages():
    """Get available languages from freee_a11y_gl configuration."""
    try:
        # Use Config method for consistent access
        return Config.get_available_languages()
    except:
        # Fallback for cases where settings are not initialized
        return ["ja", "en"]

# For backward compatibility
AVAILABLE_LANGUAGES = get_available_languages()
