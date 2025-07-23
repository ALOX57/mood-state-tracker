"""
Tests input handling functions for moods, notes, and tags.

Includes tests for parsing comma-separated tags and ensuring correct normalisation
(e.g. trimming spaces, converting to lowercase, filtering out blanks).
"""

from moodtracker.input_handler import get_tags


def test_get_tags_basic(monkeypatch):
    """Test tag input parsing. Ensures whitespace is stripped and tags are normalized."""
    monkeypatch.setattr("builtins.input", lambda _: " Happy, tired  ,  ")

    tags = get_tags()

    assert tags == ["happy", "tired"]