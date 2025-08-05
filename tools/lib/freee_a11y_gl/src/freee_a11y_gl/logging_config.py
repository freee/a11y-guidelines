"""Logging configuration for freee_a11y_gl module."""
import logging
import sys
from typing import Optional


class FreeeA11yGlLogger:
    """Centralized logging configuration for freee_a11y_gl."""
    
    _instance: Optional['FreeeA11yGlLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'FreeeA11yGlLogger':
        """Ensure singleton pattern for logger."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logger with default configuration."""
        self._logger = logging.getLogger('freee_a11y_gl')
        self._logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if not self._logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(logging.WARNING)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            self._logger.addHandler(console_handler)
    
    @property
    def logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self._logger
    
    def set_level(self, level: int) -> None:
        """Set the logging level.
        
        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)
    
    def add_file_handler(self, file_path: str, level: int = logging.INFO) -> None:
        """Add a file handler to the logger.
        
        Args:
            file_path: Path to the log file
            level: Logging level for the file handler
        """
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)


def get_logger() -> logging.Logger:
    """Get the freee_a11y_gl logger instance.
    
    Returns:
        The configured logger instance
    """
    logger_instance = FreeeA11yGlLogger()
    return logger_instance.logger
