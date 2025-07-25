"""
Main entry point for the Mood Tracker CLI application.

Handles user interaction flow, captures input, stores data, and logs errors if they occur.
"""

import sys
from config import DB_PATH
from datetime import datetime
import os
from moodtracker.db import insert_mood, get_connection
from moodtracker.logger import log_error_to_file
from moodtracker.input_handler import get_valid_mood_input, get_optional_note, get_tags
from moodtracker.query import get_all_moods, get_moods_by_tag
from moodtracker.cli_utils import display_moods


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
    elif command == "filter":
        return handle_filter(sys.argv[2:])
    elif command == "stats":
        return handle_stats()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [log | view | filter| stats]")
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
        with get_connection() as conn:
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
        with get_connection() as conn:
            moods = get_all_moods(conn)
        if not moods:
            print("No moods found")
        else:
            display_moods(moods, "Mood Entries")
        return 0

    except Exception as e:
        print("ERROR: Failed to retrieve moods.")
        print(e)
        log_error_to_file(e)
        return 1


def handle_filter(args: list[str]) -> int:
    if len(args) != 2 or args[0] != "--tag":
        print("Usage: python main.py filter --tag TAG")
        return 1

    tag = args[1]

    try:
        with get_connection() as conn:
            moods = get_moods_by_tag(conn, tag)

            if not moods:
                print(f"No moods found with tag: {tag}")
            else:
                display_moods(moods, f"Mood Entries Tagged '{tag}'")
            return 0

    except Exception as e:
        print("ERROR: Failed to filter moods.")
        print(e)
        log_error_to_file(e)
        return 1


def handle_stats() -> int:
    try:
        with get_connection() as conn:
            moods = get_all_moods(conn)

            if not moods:
                print("No data available.")
                return 0

            scores = [int(row[2]) for row in moods]
            print("\n=== Mood Statistics ===")
            print(f"Total entries: {len(scores)}")
            print(f"Average mood: {sum(scores) / len(scores):.2f}")
            print(f"Lowest mood: {min(scores)}")
            print(f"Highest mood: {max(scores)}")

            return 0
    except Exception as e:
        print("ERROR: Failed to retrieve statistics")
        print(e)
        log_error_to_file(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
