"""
Logging utilities for the logic package.

This module provides consistent logging configuration across the logic package.
It offers functions to create and configure loggers with consistent formatting,
as well as to control the logging level globally for the entire package.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Creates or retrieves a logger with the given name and configures it
    with appropriate formatting and log level.

    Args:
        name: Name of the logger (typically module name)
        level: Logging level (if None, uses INFO)

    Returns:
        Configured logger instance ready for use
    """
    logger = logging.getLogger(name)

    # Set default level if not already configured
    if level is not None:
        logger.setLevel(level)
    elif not logger.hasHandlers():
        logger.setLevel(logging.INFO)

    # Add handler if none exists
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Create a module-level logger for direct import
logger = get_logger("logic")


def set_global_log_level(level: int) -> None:
    """
    Set the log level for all loggers in the logic package.

    This function affects all existing loggers in the logic namespace
    and sets their level to the specified value.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            Example: logging.DEBUG or logging.ERROR

    Example:
        >>> from logic.utils.logger import set_global_log_level
        >>> import logging
        >>> set_global_log_level(logging.DEBUG)  # Enable debug logging
    """
    # Update root logger for the package
    logging.getLogger("logic").setLevel(level)

    # Also update the module-level logger
    logger.setLevel(level)
