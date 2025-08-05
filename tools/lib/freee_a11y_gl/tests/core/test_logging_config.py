"""Tests for logging configuration."""
import logging
import tempfile
from unittest.mock import patch, Mock

import pytest

from freee_a11y_gl.logging_config import FreeeA11yGlLogger, get_logger


class TestFreeeA11yGlLogger:
    """Test cases for FreeeA11yGlLogger class."""

    def setup_method(self):
        """Reset logger instance before each test."""
        # Clear the singleton instance
        FreeeA11yGlLogger._instance = None
        FreeeA11yGlLogger._logger = None

    def test_singleton_pattern(self):
        """Test that FreeeA11yGlLogger follows singleton pattern."""
        logger1 = FreeeA11yGlLogger()
        logger2 = FreeeA11yGlLogger()
        
        assert logger1 is logger2
        assert logger1.logger is logger2.logger

    def test_logger_initialization(self):
        """Test logger is properly initialized."""
        logger_instance = FreeeA11yGlLogger()
        logger = logger_instance.logger
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == 'freee_a11y_gl'
        assert logger.level == logging.INFO

    def test_logger_has_console_handler(self):
        """Test that logger has a console handler."""
        logger_instance = FreeeA11yGlLogger()
        logger = logger_instance.logger
        
        assert len(logger.handlers) >= 1
        
        # Check if any handler is a StreamHandler (console handler)
        has_console_handler = any(
            isinstance(handler, logging.StreamHandler) 
            for handler in logger.handlers
        )
        assert has_console_handler

    def test_set_level(self):
        """Test setting logging level."""
        logger_instance = FreeeA11yGlLogger()
        logger_instance.set_level(logging.DEBUG)
        
        assert logger_instance.logger.level == logging.DEBUG
        
        # Check that handlers also have the level set
        for handler in logger_instance.logger.handlers:
            assert handler.level == logging.DEBUG

    def test_add_file_handler(self):
        """Test adding a file handler."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as tmp_file:
            log_file_path = tmp_file.name
        
        try:
            logger_instance = FreeeA11yGlLogger()
            initial_handler_count = len(logger_instance.logger.handlers)
            
            logger_instance.add_file_handler(log_file_path, logging.ERROR)
            
            # Should have one more handler
            assert len(logger_instance.logger.handlers) == initial_handler_count + 1
            
            # Check that the new handler is a FileHandler
            file_handlers = [
                handler for handler in logger_instance.logger.handlers
                if isinstance(handler, logging.FileHandler)
            ]
            assert len(file_handlers) >= 1
            
            # Check the level of the file handler
            file_handler = file_handlers[-1]  # Get the last added file handler
            assert file_handler.level == logging.ERROR
            
        finally:
            # Clean up the temporary file
            import os
            try:
                os.unlink(log_file_path)
            except OSError:
                pass

    def test_multiple_initializations_same_instance(self):
        """Test that multiple initializations return the same instance."""
        logger1 = FreeeA11yGlLogger()
        logger2 = FreeeA11yGlLogger()
        logger3 = FreeeA11yGlLogger()
        
        assert logger1 is logger2 is logger3
        assert logger1._logger is logger2._logger is logger3._logger

    def test_no_duplicate_handlers(self):
        """Test that multiple initializations don't create duplicate handlers."""
        logger1 = FreeeA11yGlLogger()
        initial_handler_count = len(logger1.logger.handlers)
        
        logger2 = FreeeA11yGlLogger()
        
        # Should not have duplicate handlers
        assert len(logger2.logger.handlers) == initial_handler_count

    def test_logger_formatter(self):
        """Test that handlers have proper formatters."""
        logger_instance = FreeeA11yGlLogger()
        logger = logger_instance.logger
        
        for handler in logger.handlers:
            formatter = handler.formatter
            assert formatter is not None
            
            # Test the format by creating a dummy log record
            record = logging.LogRecord(
                name='test',
                level=logging.INFO,
                pathname='test.py',
                lineno=1,
                msg='Test message',
                args=(),
                exc_info=None
            )
            
            formatted = formatter.format(record)
            assert 'test' in formatted
            assert 'INFO' in formatted
            assert 'Test message' in formatted


class TestGetLogger:
    """Test cases for get_logger function."""

    def setup_method(self):
        """Reset logger instance before each test."""
        # Clear the singleton instance
        FreeeA11yGlLogger._instance = None
        FreeeA11yGlLogger._logger = None

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger()
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == 'freee_a11y_gl'

    def test_get_logger_singleton_behavior(self):
        """Test that get_logger returns the same logger instance."""
        logger1 = get_logger()
        logger2 = get_logger()
        
        assert logger1 is logger2

    def test_get_logger_consistency_with_class(self):
        """Test that get_logger returns same logger as class instance."""
        function_logger = get_logger()
        class_logger = FreeeA11yGlLogger().logger
        
        assert function_logger is class_logger

    @patch('freee_a11y_gl.logging_config.FreeeA11yGlLogger')
    def test_get_logger_creates_instance(self, mock_logger_class):
        """Test that get_logger creates FreeeA11yGlLogger instance."""
        mock_instance = Mock()
        mock_logger = Mock()
        mock_instance.logger = mock_logger
        mock_logger_class.return_value = mock_instance
        
        result = get_logger()
        
        mock_logger_class.assert_called_once()
        assert result is mock_logger

    def test_logging_functionality(self):
        """Test basic logging functionality."""
        logger = get_logger()
        
        # Test that we can call logging methods without errors
        # We can't easily test the output without capturing it,
        # but we can ensure the methods don't raise exceptions
        try:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")
        except Exception as e:
            pytest.fail(f"Logging method raised an exception: {e}")

    def test_logger_level_hierarchy(self):
        """Test that logger respects level hierarchy."""
        logger = get_logger()
        
        # Set to WARNING level
        logger.setLevel(logging.WARNING)
        
        # These should be the effective levels
        assert not logger.isEnabledFor(logging.DEBUG)
        assert not logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)
        assert logger.isEnabledFor(logging.CRITICAL)