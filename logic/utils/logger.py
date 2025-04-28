import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger (typically module name)
        level: Logging level (if None, uses INFO)

    Returns:
        Configured logger instance
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

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Update root logger for the package
    logging.getLogger("logic").setLevel(level)

    # Also update the module-level logger
    logger.setLevel(level)
