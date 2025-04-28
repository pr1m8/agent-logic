"""
Utilities module for the logic package.

This package contains utility functions and helpers used throughout the logic package.
It includes:
- logger: Standardized logging configuration and utility functions
- Other utility modules may be added in the future
"""

from .logger import get_logger, set_global_log_level

__all__ = ["get_logger", "set_global_log_level"]
