"""Input validation utilities for freee_a11y_gl module."""
import re
from typing import Any, Dict, List, Optional
from .exceptions import ValidationError
from .logging_config import get_logger

logger = get_logger()


class InputValidator:
    """Comprehensive input validation utilities."""
    
    # Regular expressions for common patterns
    ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    LANGUAGE_CODE_PATTERN = re.compile(r'^[a-z]{2}$')
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    PATH_PATTERN = re.compile(r'^/[a-zA-Z0-9_\-/]*/$')
    
    @classmethod
    def validate_id(cls, value: str, field_name: str = "ID") -> str:
        """Validate ID format.
        
        Args:
            value: The ID value to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated ID value
            
        Raises:
            ValidationError: If ID format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if not value:
            raise ValidationError(f"{field_name} cannot be empty")
        
        if not cls.ID_PATTERN.match(value):
            raise ValidationError(
                f"{field_name} must contain only alphanumeric characters, "
                f"hyphens, and underscores: {value}"
            )
        
        logger.debug(f"Validated {field_name}: {value}")
        return value
    
    @classmethod
    def validate_language_code(cls, value: str) -> str:
        """Validate language code format.
        
        Args:
            value: The language code to validate
            
        Returns:
            The validated language code
            
        Raises:
            ValidationError: If language code format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError("Language code must be a string")
        
        if not cls.LANGUAGE_CODE_PATTERN.match(value):
            raise ValidationError(
                f"Language code must be 2 lowercase letters: {value}"
            )
        
        logger.debug(f"Validated language code: {value}")
        return value
    
    @classmethod
    def validate_url(cls, value: str, field_name: str = "URL") -> str:
        """Validate URL format.
        
        Args:
            value: The URL to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated URL
            
        Raises:
            ValidationError: If URL format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if not value:
            raise ValidationError(f"{field_name} cannot be empty")
        
        if not cls.URL_PATTERN.match(value):
            raise ValidationError(f"Invalid {field_name} format: {value}")
        
        logger.debug(f"Validated {field_name}: {value}")
        return value
    
    @classmethod
    def validate_path(cls, value: str, field_name: str = "Path") -> str:
        """Validate path format.
        
        Args:
            value: The path to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated path
            
        Raises:
            ValidationError: If path format is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if not value:
            raise ValidationError(f"{field_name} cannot be empty")
        
        if not value.startswith('/'):
            raise ValidationError(f"{field_name} must start with /: {value}")
        
        if not value.endswith('/'):
            raise ValidationError(f"{field_name} must end with /: {value}")
        
        logger.debug(f"Validated {field_name}: {value}")
        return value
    
    @classmethod
    def validate_non_empty_string(cls, value: str, field_name: str) -> str:
        """Validate that a string is not empty.
        
        Args:
            value: The string to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated string
            
        Raises:
            ValidationError: If string is empty or not a string
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if not value.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        
        logger.debug(f"Validated {field_name}: {value}")
        return value
    
    @classmethod
    def validate_dict(cls, value: Any, field_name: str) -> Dict[str, Any]:
        """Validate that a value is a dictionary.
        
        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated dictionary
            
        Raises:
            ValidationError: If value is not a dictionary
        """
        if not isinstance(value, dict):
            raise ValidationError(f"{field_name} must be a dictionary")
        
        logger.debug(f"Validated {field_name}: {type(value).__name__}")
        return value
    
    @classmethod
    def validate_list(cls, value: Any, field_name: str) -> List[Any]:
        """Validate that a value is a list.
        
        Args:
            value: The value to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated list
            
        Raises:
            ValidationError: If value is not a list
        """
        if not isinstance(value, list):
            raise ValidationError(f"{field_name} must be a list")
        
        logger.debug(f"Validated {field_name}: {type(value).__name__}")
        return value
    
    @classmethod
    def validate_optional_string(cls, value: Optional[str], 
                                 field_name: str) -> Optional[str]:
        """Validate an optional string value.
        
        Args:
            value: The optional string to validate
            field_name: Name of the field for error messages
            
        Returns:
            The validated optional string
            
        Raises:
            ValidationError: If value is not None and not a string
        """
        if value is not None and not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string or None")
        
        logger.debug(f"Validated optional {field_name}: {value}")
        return value
    
    @classmethod
    def validate_enum(cls, value: str, valid_values: List[str], 
                      field_name: str) -> str:
        """Validate that a value is in a list of valid values.
        
        Args:
            value: The value to validate
            valid_values: List of valid values
            field_name: Name of the field for error messages
            
        Returns:
            The validated value
            
        Raises:
            ValidationError: If value is not in valid_values
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if value not in valid_values:
            raise ValidationError(
                f"{field_name} must be one of {valid_values}: {value}"
            )
        
        logger.debug(f"Validated {field_name}: {value}")
        return value
