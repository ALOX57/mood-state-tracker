"""
Unit tests for database initialization and mood/tag insertion logic.
Covers:
- Creating the database schema
- Inserting moods with and without tags/notes
- Tag normalization and deduplication
- Tag reuse across entries
- Data integrity checks
"""

from moodtracker.db import init_db, insert_mood


def test_insert_mood_with_tags():
    """Test inserting a mood with multiple tags. Ensures correct link creation in join table."""
    conn = init_db(":memory:")

    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "7"
    note = "just testing"
    tags = ["tired", "focused"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    # 1. Check logs table
    cursor.execute("SELECT COUNT(*) FROM moods")
    assert cursor.fetchone()[0] == 1

    # 2. Check tags
    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 2

    # 3. Check join table
    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 2

    conn.close()


def test_insert_mood_without_tags():
    """Test inserting a mood entry without tags. Verifies no join entries are created."""
    conn = init_db(":memory:")

    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "5"
    note = "No tags today"
    tags = []

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM moods")
    assert cursor.fetchone()[0] == 1

    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 0

    conn.close()


def test_duplicate_tag_input():
    """Test handling of duplicate tag input. Only one tag should be stored and linked."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "6"
    note = "Feeling... redundant"
    tags = ["happy", "happy"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 1

    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 1

    conn.close()


def test_tag_case_insensitivity():
    """Test normalization of tag case. Variants of the same tag should be treated as one."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "9"
    note = "Mixed case feelings"
    tags = ["Happy", "happy", "HAPPY"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 1

    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 1

    conn.close()


def test_tags_with_only_spaces():
    """Test that whitespace-only tags are ignored and not inserted."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"

    insert_mood(conn, timestamp, "5", "test", ["   ", "real", " "])

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 1  # only 'real' should be stored

    conn.close()


def test_multiple_moods_shared_tag():
    """Test inserting multiple moods with a shared tag. Tag should not duplicate, but links should."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"

    insert_mood(conn, timestamp, "7", "first", ["shared"])
    insert_mood(conn, timestamp, "6", "second", ["shared"])

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 1  # only one tag

    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 2  # two mood-tag links

    conn.close()


def test_insert_exact_mood_and_note():
    """Test that the correct mood and note values are inserted and retrievable."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "8"
    note = "Felt okay today"
    tags = ["calm", "neutral"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    # Check exact values
    cursor.execute("SELECT mood, mood_note FROM moods")
    row = cursor.fetchone()
    assert row == (mood, note)

    conn.close()


def test_insert_mood_without_note():
    """Test inserting a mood without a note. Mood note should be stored as an empty string."""
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "6"
    note = ""
    tags = ["blank"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT mood_note FROM moods")
    note_value = cursor.fetchone()[0]
    assert note_value == ""

    conn.close()


def test_tables_exist_after_init():
    """Test that all required tables are created during database initialization."""
    conn = init_db(":memory:")
    cursor = conn.cursor()

    for table in ["moods", "tags", "mood_tags"]:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        assert cursor.fetchone() is not None

    conn.close()
