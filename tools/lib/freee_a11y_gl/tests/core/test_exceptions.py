"""Tests for custom exception classes."""
import pytest

from freee_a11y_gl.exceptions import (
    FreeeA11yGlError,
    ConfigurationError,
    ValidationError,
    DataError,
    FileOperationError,
    ResourceNotFoundError,
    DuplicateIdError,
    ReferenceError,
    VersionError,
    InfoUtilsError,
    MessageCatalogError
)


class TestFreeeA11yGlError:
    """Test cases for FreeeA11yGlError base exception."""

    def test_basic_creation(self):
        """Test basic exception creation."""
        error = FreeeA11yGlError("Test message")
        
        assert error.message == "Test message"
        assert error.details is None
        assert str(error) == "Test message"

    def test_creation_with_details(self):
        """Test exception creation with details."""
        error = FreeeA11yGlError("Test message", "Additional details")
        
        assert error.message == "Test message"
        assert error.details == "Additional details"
        assert str(error) == "Test message\nDetails: Additional details"

    def test_inheritance(self):
        """Test that FreeeA11yGlError inherits from Exception."""
        error = FreeeA11yGlError("Test message")
        
        assert isinstance(error, Exception)
        assert isinstance(error, FreeeA11yGlError)

    def test_can_be_raised(self):
        """Test that exception can be raised and caught."""
        with pytest.raises(FreeeA11yGlError) as exc_info:
            raise FreeeA11yGlError("Test error")
        
        assert exc_info.value.message == "Test error"

    def test_can_be_caught_as_exception(self):
        """Test that exception can be caught as generic Exception."""
        with pytest.raises(Exception) as exc_info:
            raise FreeeA11yGlError("Test error")
        
        assert isinstance(exc_info.value, FreeeA11yGlError)


class TestSpecificExceptions:
    """Test cases for specific exception classes."""

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config error", "Config details")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, ConfigurationError)
        assert error.message == "Config error"
        assert error.details == "Config details"

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation failed")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, ValidationError)
        assert error.message == "Validation failed"

    def test_data_error(self):
        """Test DataError."""
        error = DataError("Data error")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, DataError)
        assert error.message == "Data error"

    def test_file_operation_error(self):
        """Test FileOperationError."""
        error = FileOperationError("File operation failed")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, FileOperationError)
        assert error.message == "File operation failed"

    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError."""
        error = ResourceNotFoundError("Resource not found")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, ResourceNotFoundError)
        assert error.message == "Resource not found"

    def test_duplicate_id_error(self):
        """Test DuplicateIdError."""
        error = DuplicateIdError("Duplicate ID detected")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, DataError)  # Should inherit from DataError
        assert isinstance(error, DuplicateIdError)
        assert error.message == "Duplicate ID detected"

    def test_reference_error(self):
        """Test ReferenceError."""
        error = ReferenceError("Invalid reference")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, DataError)  # Should inherit from DataError
        assert isinstance(error, ReferenceError)
        assert error.message == "Invalid reference"

    def test_version_error(self):
        """Test VersionError."""
        error = VersionError("Version error")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, VersionError)
        assert error.message == "Version error"

    def test_info_utils_error(self):
        """Test InfoUtilsError."""
        error = InfoUtilsError("Info utils error")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, InfoUtilsError)
        assert error.message == "Info utils error"

    def test_message_catalog_error(self):
        """Test MessageCatalogError."""
        error = MessageCatalogError("Message catalog error")
        
        assert isinstance(error, FreeeA11yGlError)
        assert isinstance(error, MessageCatalogError)
        assert error.message == "Message catalog error"


class TestExceptionHierarchy:
    """Test cases for exception hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all custom exceptions inherit from FreeeA11yGlError."""
        exception_classes = [
            ConfigurationError,
            ValidationError,
            DataError,
            FileOperationError,
            ResourceNotFoundError,
            DuplicateIdError,
            ReferenceError,
            VersionError,
            InfoUtilsError,
            MessageCatalogError
        ]
        
        for exc_class in exception_classes:
            error = exc_class("Test message")
            assert isinstance(error, FreeeA11yGlError)

    def test_data_error_subclasses(self):
        """Test that data-related errors inherit from DataError."""
        data_error_subclasses = [
            DuplicateIdError,
            ReferenceError
        ]
        
        for exc_class in data_error_subclasses:
            error = exc_class("Test message")
            assert isinstance(error, DataError)
            assert isinstance(error, FreeeA11yGlError)

    def test_exception_catching_hierarchy(self):
        """Test that exceptions can be caught at different hierarchy levels."""
        # Test catching specific exception
        with pytest.raises(DuplicateIdError):
            raise DuplicateIdError("Duplicate ID")
        
        # Test catching parent class
        with pytest.raises(DataError):
            raise DuplicateIdError("Duplicate ID")
        
        # Test catching base class
        with pytest.raises(FreeeA11yGlError):
            raise DuplicateIdError("Duplicate ID")
        
        # Test catching as generic Exception
        with pytest.raises(Exception):
            raise DuplicateIdError("Duplicate ID")


class TestExceptionUsage:
    """Test cases for practical exception usage."""

    def test_exception_with_context(self):
        """Test using exceptions in a try-except context."""
        def risky_operation():
            raise ConfigurationError("Invalid config", "Missing required field")
        
        try:
            risky_operation()
        except ConfigurationError as e:
            assert e.message == "Invalid config"
            assert e.details == "Missing required field"
            assert "Invalid config\nDetails: Missing required field" in str(e)
        else:
            pytest.fail("Expected ConfigurationError was not raised")

    def test_exception_chaining(self):
        """Test exception chaining with raise from."""
        def inner_operation():
            raise ValueError("Original error")
        
        def outer_operation():
            try:
                inner_operation()
            except ValueError as e:
                raise ConfigurationError("Config failed") from e
        
        with pytest.raises(ConfigurationError) as exc_info:
            outer_operation()
        
        assert exc_info.value.message == "Config failed"
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ValueError)

    def test_multiple_exception_types(self):
        """Test handling multiple exception types."""
        def operation_that_can_fail(error_type):
            if error_type == "validation":
                raise ValidationError("Validation failed")
            elif error_type == "config":
                raise ConfigurationError("Config failed")
            elif error_type == "data":
                raise DataError("Data error")
            else:
                return "success"
        
        # Test successful operation
        result = operation_that_can_fail("success")
        assert result == "success"
        
        # Test different error types
        with pytest.raises(ValidationError):
            operation_that_can_fail("validation")
        
        with pytest.raises(ConfigurationError):
            operation_that_can_fail("config")
        
        with pytest.raises(DataError):
            operation_that_can_fail("data")