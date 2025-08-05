"""Custom exception classes for freee_a11y_gl module."""


class FreeeA11yGlError(Exception):
    """Base exception class for all freee_a11y_gl related errors."""
    
    def __init__(self, message: str, details: str = None):
        """Initialize the exception.
        
        Args:
            message: The error message
            details: Additional error details
        """
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


class ConfigurationError(FreeeA11yGlError):
    """Exception raised for configuration-related errors."""
    pass


class ValidationError(FreeeA11yGlError):
    """Exception raised for validation errors."""
    pass


class DataError(FreeeA11yGlError):
    """Exception raised for data-related errors."""
    pass


class FileOperationError(FreeeA11yGlError):
    """Exception raised for file operation errors."""
    pass


class ResourceNotFoundError(FreeeA11yGlError):
    """Exception raised when a required resource is not found."""
    pass


class DuplicateIdError(DataError):
    """Exception raised when duplicate IDs are detected."""
    pass


class ReferenceError(DataError):
    """Exception raised when references to non-existent items are found."""
    pass


class VersionError(FreeeA11yGlError):
    """Exception raised for version-related errors."""
    pass


class InfoUtilsError(FreeeA11yGlError):
    """Exception raised for info utilities related errors."""
    pass


class MessageCatalogError(FreeeA11yGlError):
    """Exception raised for message catalog related errors."""
    pass
