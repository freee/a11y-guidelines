"""Base generator class for generating RST content from data."""
from typing import Dict, Any, Iterator, Optional

class BaseGenerator:
    """Base class for all content generators."""
    
    def __init__(self, lang: str):
        """Initialize the generator.
        
        Args:
            lang: Language code for content generation
        """
        self.lang = lang

    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate content data.
        
        Returns:
            Iterator yielding dictionaries containing template data
        """
        raise NotImplementedError("Subclasses must implement generate()")

    def get_dependencies(self) -> list[str]:
        """Get list of file dependencies for this generator.
        
        Returns:
            List of file paths that this generator depends on
        """
        return []
