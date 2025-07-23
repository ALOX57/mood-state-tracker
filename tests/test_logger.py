"""
Tests the error logging utility to ensure exceptions are correctly written
to the configured log file path.
"""

import os
from moodtracker import logger


def test_log_error_to_file(monkeypatch):
    """
    Test that log_error_to_file writes exception trace to the configured log path.

    This test monkeypatches the logger's ERROR_LOG_PATH to a temporary test file, raises a fake exception,
    and verifies that the log file is created and contains the expected error message.
    """

    test_path = "tests/temp_test_log.log"

    # Monkeypatch the ERROR_LOG_PATH to use test path
    monkeypatch.setattr(logger, "ERROR_LOG_PATH", test_path)

    # Clean up old test log if exists
    if os.path.exists(test_path):
        os.remove(test_path)

    try:
        raise ValueError("Fake test error")
    except Exception as e:
        logger.log_error_to_file(e)

    # Check the file was created and includes the error text
    assert os.path.exists(test_path)

    with open(test_path, "r") as f:
        content = f.read()
        assert "ValueError: Fake test error" in content
