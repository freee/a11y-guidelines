"""Tests for error recovery mechanisms."""
import os
import tempfile
import time
from unittest.mock import Mock, patch, mock_open

import pytest

from freee_a11y_gl.error_recovery import ErrorRecovery
from freee_a11y_gl.exceptions import (
    FreeeA11yGlError, 
    ConfigurationError, 
    FileOperationError
)


class TestErrorRecovery:
    """Test cases for ErrorRecovery class."""

    def test_with_fallback_primary_success(self):
        """Test with_fallback when primary function succeeds."""
        primary_func = Mock(return_value="primary_result")
        fallback_func = Mock()
        
        result = ErrorRecovery.with_fallback(
            primary_func, fallback_func, "Test operation"
        )
        
        assert result == "primary_result"
        primary_func.assert_called_once()
        fallback_func.assert_not_called()

    def test_with_fallback_primary_fails_fallback_succeeds(self):
        """Test with_fallback when primary fails but fallback succeeds."""
        primary_func = Mock(side_effect=ValueError("Primary failed"))
        fallback_func = Mock(return_value="fallback_result")
        
        result = ErrorRecovery.with_fallback(
            primary_func, fallback_func, "Test operation"
        )
        
        assert result == "fallback_result"
        primary_func.assert_called_once()
        fallback_func.assert_called_once()

    def test_with_fallback_both_fail(self):
        """Test with_fallback when both primary and fallback fail."""
        primary_func = Mock(side_effect=ValueError("Primary failed"))
        fallback_func = Mock(side_effect=RuntimeError("Fallback failed"))
        
        with pytest.raises(FreeeA11yGlError) as exc_info:
            ErrorRecovery.with_fallback(
                primary_func, fallback_func, "Test operation"
            )
        
        assert "Both primary and fallback operations failed" in str(exc_info.value)
        assert "Primary: Primary failed" in exc_info.value.details
        assert "Fallback: Fallback failed" in exc_info.value.details

    def test_safe_file_operation_success(self):
        """Test safe_file_operation with successful operation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test content")
            tmp_file_path = tmp_file.name
        
        try:
            def read_file(path):
                with open(path, 'r') as f:
                    return f.read()
            
            result = ErrorRecovery.safe_file_operation(
                tmp_file_path, read_file
            )
            
            assert result == "test content"
        
        finally:
            os.unlink(tmp_file_path)

    def test_safe_file_operation_file_not_found_with_fallback(self):
        """Test safe_file_operation with missing file and fallback value."""
        def read_file(path):
            with open(path, 'r') as f:
                return f.read()
        
        result = ErrorRecovery.safe_file_operation(
            "/non/existent/file.txt", 
            read_file,
            fallback_value="default_content"
        )
        
        assert result == "default_content"

    def test_safe_file_operation_file_not_found_no_fallback(self):
        """Test safe_file_operation with missing file and no fallback."""
        def read_file(path):
            with open(path, 'r') as f:
                return f.read()
        
        with pytest.raises(FileOperationError) as exc_info:
            ErrorRecovery.safe_file_operation(
                "/non/existent/file.txt", 
                read_file
            )
        
        assert "File operation failed" in str(exc_info.value)

    def test_safe_file_operation_create_if_missing(self):
        """Test safe_file_operation with create_if_missing=True."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, "subdir", "new_file.txt")
            
            def write_file(path):
                with open(path, 'w') as f:
                    f.write("created content")
                return "file_created"
            
            result = ErrorRecovery.safe_file_operation(
                file_path, 
                write_file,
                create_if_missing=True
            )
            
            assert result == "file_created"
            assert os.path.exists(file_path)

    def test_safe_config_get_existing_key(self):
        """Test safe_config_get with existing key."""
        config = {"database": {"host": "localhost", "port": 5432}}
        
        result = ErrorRecovery.safe_config_get(config, "database.host")
        
        assert result == "localhost"

    def test_safe_config_get_missing_key_with_default(self):
        """Test safe_config_get with missing key and default value."""
        config = {"database": {"host": "localhost"}}
        
        result = ErrorRecovery.safe_config_get(
            config, "database.password", "default_password"
        )
        
        assert result == "default_password"

    def test_safe_config_get_missing_required_key(self):
        """Test safe_config_get with missing required key."""
        config = {"database": {"host": "localhost"}}
        
        with pytest.raises(ConfigurationError) as exc_info:
            ErrorRecovery.safe_config_get(
                config, "database.password", required=True
            )
        
        assert "Required configuration key 'database.password' not found" in str(exc_info.value)

    def test_safe_config_get_nested_missing_structure(self):
        """Test safe_config_get with missing nested structure."""
        config = {"database": "simple_string"}
        
        result = ErrorRecovery.safe_config_get(
            config, "database.host", "default_host"
        )
        
        assert result == "default_host"

    def test_retry_operation_success_first_try(self):
        """Test retry_operation succeeding on first attempt."""
        operation = Mock(return_value="success")
        
        result = ErrorRecovery.retry_operation(operation, max_retries=3)
        
        assert result == "success"
        operation.assert_called_once()

    def test_retry_operation_success_after_retries(self):
        """Test retry_operation succeeding after some failures."""
        operation = Mock(side_effect=[
            ValueError("Fail 1"),
            ValueError("Fail 2"), 
            "success"
        ])
        
        with patch('time.sleep'):  # Mock sleep to speed up test
            result = ErrorRecovery.retry_operation(operation, max_retries=3)
        
        assert result == "success"
        assert operation.call_count == 3

    def test_retry_operation_all_attempts_fail(self):
        """Test retry_operation when all attempts fail."""
        operation = Mock(side_effect=ValueError("Always fails"))
        
        with patch('time.sleep'):  # Mock sleep to speed up test
            with pytest.raises(FreeeA11yGlError) as exc_info:
                ErrorRecovery.retry_operation(operation, max_retries=2)
        
        assert "Operation failed after 3 attempts" in str(exc_info.value)
        assert operation.call_count == 3

    def test_retry_operation_with_backoff(self):
        """Test retry_operation uses exponential backoff."""
        operation = Mock(side_effect=[ValueError("Fail"), "success"])
        
        with patch('time.sleep') as mock_sleep:
            ErrorRecovery.retry_operation(
                operation, max_retries=2, delay=1.0, backoff_factor=2.0
            )
        
        # Should sleep once with delay=1.0
        mock_sleep.assert_called_once_with(1.0)

    def test_graceful_degradation_preferred_succeeds(self):
        """Test graceful_degradation when preferred implementation succeeds."""
        preferred_func = Mock(return_value="preferred_result")
        degraded_func = Mock()
        
        result = ErrorRecovery.graceful_degradation(
            preferred_func, degraded_func, "test_feature"
        )
        
        assert result == "preferred_result"
        preferred_func.assert_called_once()
        degraded_func.assert_not_called()

    def test_graceful_degradation_preferred_fails_degraded_succeeds(self):
        """Test graceful_degradation when preferred fails but degraded succeeds."""
        preferred_func = Mock(side_effect=RuntimeError("Preferred failed"))
        degraded_func = Mock(return_value="degraded_result")
        
        result = ErrorRecovery.graceful_degradation(
            preferred_func, degraded_func, "test_feature"
        )
        
        assert result == "degraded_result"
        preferred_func.assert_called_once()
        degraded_func.assert_called_once()

    def test_graceful_degradation_both_fail(self):
        """Test graceful_degradation when both implementations fail."""
        preferred_func = Mock(side_effect=RuntimeError("Preferred failed"))
        degraded_func = Mock(side_effect=ValueError("Degraded failed"))
        
        with pytest.raises(FreeeA11yGlError) as exc_info:
            ErrorRecovery.graceful_degradation(
                preferred_func, degraded_func, "test_feature"
            )
        
        assert "Both preferred and degraded implementations failed for test_feature" in str(exc_info.value)
        assert "Preferred: Preferred failed" in exc_info.value.details
        assert "Degraded: Degraded failed" in exc_info.value.details