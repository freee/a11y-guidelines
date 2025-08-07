"""Error recovery mechanisms for freee_a11y_gl module."""
import os
from typing import Any, Dict, Callable
from .exceptions import FreeeA11yGlError, ConfigurationError, FileOperationError
from .logging_config import get_logger

logger = get_logger()


class ErrorRecovery:
    """Provides error recovery mechanisms and fallback strategies."""

    @staticmethod
    def with_fallback(primary_func: Callable[[], Any],
                      fallback_func: Callable[[], Any],
                      error_message: str = "Primary operation failed") -> Any:
        """Execute a function with a fallback if it fails.

        Args:
            primary_func: The primary function to execute
            fallback_func: The fallback function to execute if primary fails
            error_message: Error message to log

        Returns:
            Result from primary function or fallback function
        """
        try:
            logger.debug("Attempting primary operation")
            return primary_func()
        except Exception as e:
            logger.warning(f"{error_message}: {e}. Using fallback.")
            try:
                return fallback_func()
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                raise FreeeA11yGlError(
                    "Both primary and fallback operations failed",
                    f"Primary: {e}, Fallback: {fallback_error}"
                )

    @staticmethod
    def safe_file_operation(file_path: str, operation: Callable[[str], Any],
                            fallback_value: Any = None,
                            create_if_missing: bool = False) -> Any:
        """Safely perform a file operation with error recovery.

        Args:
            file_path: Path to the file
            operation: Function that takes file_path and returns a result
            fallback_value: Value to return if operation fails
            create_if_missing: Whether to create the file if it doesn't exist

        Returns:
            Result of the operation or fallback_value

        Raises:
            FileOperationError: If operation fails and no fallback is provided
        """
        try:
            if not os.path.exists(file_path):
                if create_if_missing:
                    logger.info(f"Creating missing file: {file_path}")
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w') as f:
                        f.write("")
                else:
                    raise FileNotFoundError(f"File not found: {file_path}")

            logger.debug(f"Performing file operation on: {file_path}")
            return operation(file_path)

        except Exception as e:
            logger.warning(f"File operation failed for {file_path}: {e}")

            if fallback_value is not None:
                logger.info(f"Using fallback value for {file_path}")
                return fallback_value

            raise FileOperationError(
                f"File operation failed for {file_path}",
                str(e)
            )

    @staticmethod
    def safe_config_get(config_dict: Dict[str, Any],
                        key: str,
                        default_value: Any = None,
                        required: bool = False) -> Any:
        """Safely get a configuration value with error recovery.

        Args:
            config_dict: Configuration dictionary
            key: Configuration key (supports dot notation)
            default_value: Default value if key is not found
            required: Whether the key is required

        Returns:
            Configuration value or default_value

        Raises:
            ConfigurationError: If required key is not found
        """
        try:
            # Support dot notation for nested keys
            keys = key.split('.')
            value = config_dict

            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    raise KeyError(f"Key '{key}' not found")

            logger.debug(f"Retrieved config value for '{key}': {value}")
            return value

        except (KeyError, TypeError) as e:
            logger.debug(f"Config key '{key}' not found: {e}")

            if required:
                raise ConfigurationError(
                    f"Required configuration key '{key}' not found",
                    str(e)
                )

            logger.debug(f"Using default value for '{key}': {default_value}")
            return default_value

    @staticmethod
    def retry_operation(operation: Callable[[], Any],
                        max_retries: int = 3,
                        delay: float = 1.0,
                        backoff_factor: float = 2.0) -> Any:
        """Retry an operation with exponential backoff.

        Args:
            operation: The operation to retry
            max_retries: Maximum number of retries
            delay: Initial delay between retries in seconds
            backoff_factor: Factor to multiply delay by for each retry

        Returns:
            Result of the operation

        Raises:
            FreeeA11yGlError: If all retries fail
        """
        import time

        last_exception = None
        current_delay = delay

        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    logger.info(f"Retry attempt {attempt}/{max_retries}")
                    time.sleep(current_delay)
                    current_delay *= backoff_factor

                return operation()

            except Exception as e:
                last_exception = e
                logger.warning(f"Operation failed (attempt {attempt + 1}): {e}")

                if attempt == max_retries:
                    break

        raise FreeeA11yGlError(
            f"Operation failed after {max_retries + 1} attempts",
            str(last_exception)
        )

    @staticmethod
    def graceful_degradation(preferred_func: Callable[[], Any],
                             degraded_func: Callable[[], Any],
                             feature_name: str) -> Any:
        """Implement graceful degradation for a feature.

        Args:
            preferred_func: The preferred implementation
            degraded_func: The degraded implementation
            feature_name: Name of the feature for logging

        Returns:
            Result from preferred or degraded implementation
        """
        try:
            logger.debug(f"Attempting preferred implementation for {feature_name}")
            return preferred_func()
        except Exception as e:
            logger.warning(
                f"Preferred implementation for {feature_name} failed: {e}. "
                f"Using degraded implementation."
            )
            try:
                return degraded_func()
            except Exception as degraded_error:
                logger.error(
                    f"Degraded implementation for {feature_name} also failed: "
                    f"{degraded_error}"
                )
                raise FreeeA11yGlError(
                    f"Both preferred and degraded implementations failed "
                    f"for {feature_name}",
                    f"Preferred: {e}, Degraded: {degraded_error}"
                )
