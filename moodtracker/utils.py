"""Utility functions for mood tracker."""

from datetime import datetime


def format_timestamp(iso_str: str) -> str:
    """
    Convert ISO timestamp to a human-readable format

    Args:
        iso_str (str): ISO 8601 datetime string.

    Returns:
        str: Formatted timestamp like 'Wed 23 Jul 2025 - 11:19 PM'
    """

    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%a %d %b %Y — %I:%M %p")
