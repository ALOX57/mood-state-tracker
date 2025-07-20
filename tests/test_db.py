from moodtracker.db import init_db, insert_mood


def test_insert_mood_with_tags():
    conn = init_db(":memory:")

    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "7"
    note = "just testing"
    tags = ["tired", "focused"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    # 1. Check logs table
    cursor.execute("SELECT COUNT(*) FROM logs")
    assert cursor.fetchone()[0] == 1

    # 2. Check tags
    cursor.execute("SELECT COUNT(*) FROM tags")
    assert cursor.fetchone()[0] == 2

    # 3. Check join table
    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 2

    conn.close()


def test_insert_mood_without_tags():
    conn = init_db(":memory:")

    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "5"
    note = "No tags today"
    tags = []

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    assert cursor.fetchone()[0] == 1

    cursor.execute("SELECT COUNT(*) FROM mood_tags")
    assert cursor.fetchone()[0] == 0

    conn.close()


def test_duplicate_tag_input():
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


def test_insert_exact_mood_and_note():
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "8"
    note = "Felt okay today"
    tags = ["calm", "neutral"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    # Check exact values
    cursor.execute("SELECT mood, mood_note FROM logs")
    row = cursor.fetchone()
    assert row == (mood, note)

    conn.close()


def test_insert_mood_without_note():
    conn = init_db(":memory:")
    timestamp = "2025-07-20T12:00:00+00:00"
    mood = "6"
    note = ""
    tags = ["blank"]

    insert_mood(conn, timestamp, mood, note, tags)
    cursor = conn.cursor()

    cursor.execute("SELECT mood_note FROM logs")
    note_value = cursor.fetchone()[0]
    assert note_value == ""

    conn.close()


def test_tables_exist_after_init():
    conn = init_db(":memory:")
    cursor = conn.cursor()

    for table in ["logs", "tags", "mood_tags"]:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        assert cursor.fetchone() is not None

    conn.close()
