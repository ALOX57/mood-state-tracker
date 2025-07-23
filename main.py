"""
Main entry point for the Mood Tracker CLI application.

Handles user interaction flow, captures input, stores data, and logs errors if they occur.
"""

import sys
from config import DB_PATH
from datetime import datetime
import os
from moodtracker.db import init_db, insert_mood
from moodtracker.logger import log_error_to_file
from moodtracker.input_handler import get_valid_mood_input, get_optional_note, get_tags
from moodtracker.query import get_all_moods


def main() -> int:
    if len(sys.argv) < 2:
        print("No command given — defaulting to: log")
        command = "log"
    else:
        command = sys.argv[1]

    print(f"Command received: {command}")

    if command == "log":
        return handle_log()
    elif command == "view":
        return handle_view()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [log | view]")
        return 1


def handle_log():
    conn = None

    mood = get_valid_mood_input()
    print("You entered:", mood)

    note = get_optional_note()
    tags = get_tags()

    timestamp = datetime.now().astimezone().isoformat()

    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = init_db(DB_PATH)
        insert_mood(conn, timestamp, mood, note, tags)
        print(f"Saved to database: {DB_PATH}")
    except Exception as e:
        print("ERROR: Failed to write to database.")
        print(e)
        log_error_to_file(e)
        if conn:
            conn.rollback()
        return 1
    finally:
        if conn:
            conn.close()

    print("Saved.")
    return 0


def handle_view():
    try:
        conn = init_db(DB_PATH)
        moods = get_all_moods(conn)
        if not moods:
            print("No moods found")
        else:
            print("\n=== Mood Entries ===")
            for mood in moods:
                mood_id, timestamp, score, note, tag_str = mood
                tag_display = f"Tags: {tag_str}" if tag_str else "Tags: (none)"
                print(f"[{timestamp}] Mood: {score}  {tag_display}  Note: {note or '(none)'}")
        conn.close()
        return 0
    except Exception as e:
        print("ERROR: Failed to retrieve moods.")
        print(e)
        log_error_to_file(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
