"""
Provides utility function to log application errors to a persistent file.

This module creates directories as needed and appends timestamped error tracebacks
to help diagnose unexpected failures.

The log file path is defined in `config.py` as ERROR_LOG_PATH.
"""

from datetime import datetime
import traceback
import os
from config import ERROR_LOG_PATH


def log_error_to_file(e: Exception) -> None:
    """
       Write a formatted error trace to the error log file.

       Creates any necessary directories automatically and appends the
       error with a timestamp and a visual divider for readability.

       Args:
           e (Exception): The exception object to log.
       """
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
    with open(ERROR_LOG_PATH, "a") as f:
        f.write(datetime.now().astimezone().isoformat() + "\n")
        f.write(traceback.format_exc())
        f.write("\n" + "-" * 40 + "\n")  # Divider
