# main.py
import sys
from datetime import datetime
import os
from moodtracker.db import init_db, insert_mood
from moodtracker.logger import log_error_to_file
from moodtracker.input_handler import get_valid_mood_input, get_optional_note, get_tags
from config import DB_PATH


def main() -> int:
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


if __name__ == "__main__":
    sys.exit(main())
