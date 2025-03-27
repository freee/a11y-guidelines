"""Base generator module for RST content generation."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Iterator, Optional
import logging
from dataclasses import dataclass
from pathlib import Path

class GeneratorError(Exception):
    """Base exception for generator errors."""
    pass

class ValidationError(GeneratorError):
    """Raised when data validation fails."""
    pass

@dataclass
class GeneratorContext:
    """Context information for generators."""
    lang: str
    base_dir: Path

class BaseGenerator(ABC):
    """Base class for all content generators."""
    
    def __init__(self, lang: str, base_dir: Optional[Path] = None):
        """Initialize the generator.
        
        Args:
            lang: Language code for content generation
            base_dir: Base directory for file operations (optional)
        """
        self.context = GeneratorContext(
            lang=lang,
            base_dir=Path(base_dir) if base_dir else Path.cwd()
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def lang(self) -> str:
        """Get language code for backward compatibility."""
        return self.context.lang

    @abstractmethod
    def generate(self) -> Iterator[Dict[str, Any]]:
        """Generate content data.
        
        Yields:
            Dictionary containing template data
            
        Raises:
            GeneratorError: On generation failure
        """
        raise NotImplementedError("Subclasses must implement generate()")

    def get_dependencies(self) -> list[str]:
        """Get list of file dependencies for this generator.
        
        Returns:
            List of file paths that this generator depends on
        """
        return []

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate generated data.
        
        Args:
            data: Data to validate
            
        Returns:
            True if data is valid, False otherwise
            
        Raises:
            ValidationError: If validation fails with specific reason
        """
        return True

    def preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess data before template rendering.
        
        Args:
            data: Data to preprocess
            
        Returns:
            Preprocessed data
        """
        return data

    def postprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess data after template rendering.
        
        Args:
            data: Data to postprocess
            
        Returns:
            Postprocessed data
        """
        return data

    def process_single_item(self, item: Any) -> Dict[str, Any]:
        """Process a single item into template data.
        
        Args:
            item: Item to process
            
        Returns:
            Processed template data
            
        Raises:
            GeneratorError: On processing failure
        """
        try:
            data = self._process_item(item)
            if not data:
                self.logger.warning(f"No data generated for item: {item}")
                return {}
                
            if not self.validate_data(data):
                raise ValidationError(f"Data validation failed for item: {item}")
                
            processed_data = self.preprocess_data(data)
            return self.postprocess_data(processed_data)
            
        except Exception as e:
            self.logger.error(f"Error processing item {item}: {str(e)}")
            raise GeneratorError(f"Failed to process item: {str(e)}") from e

    def _process_item(self, item: Any) -> Dict[str, Any]:
        """Internal method to process a single item.
        
        Args:
            item: Item to process
            
        Returns:
            Processed template data
        """
        raise NotImplementedError("Implement this method if using process_single_item")

    def cleanup(self) -> None:
        """Cleanup any resources after generation."""
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
