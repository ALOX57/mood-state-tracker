# main.py
import sys
from datetime import datetime
import os
import sqlite3
import traceback

DB_FILE = 'data/logs.db'


def get_valid_mood_input() -> str:
    raw = input("Mood (1-10): ").strip()
    if not raw:
        raise ValueError("Mood cannot be empty.")
    if raw.isdigit():
        val = int(raw)
        if 1 <= val <= 10:
            return str(val)
        else:
            raise ValueError("Mood must be between 1 and 10.")
    else:
        raise ValueError("Mood must be a number between 1 and 10.")


def init_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            mood TEXT NOT NULL
        )    
        ''')
    conn.commit()
    return conn


def insert_mood(conn: sqlite3.Connection, timestamp: str, mood: str) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, mood)
        VALUES (?, ?)
    ''', (timestamp, mood))
    conn.commit()


def log_error_to_file(e: Exception):
    with open("error.log", "a") as f:
        f.write(datetime.now().astimezone().isoformat() + "\n")
        f.write(traceback.format_exc())
        f.write("\n" + "-" * 40 + "\n")  # Divider


def main():
    mood = None
    conn = None

    try:
        mood = get_valid_mood_input()
        print("You entered:", mood)
    except ValueError as e:
        print("ERROR:", e)
        return 1

    timestamp = datetime.now().astimezone().isoformat()

    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        conn = init_db(DB_FILE)
        insert_mood(conn, timestamp, mood)
        print(f"Saved to database: {DB_FILE}")
    except Exception as e:
        print("ERROR: Failed to write to database.")
        print(e)
        log_error_to_file(e)
        if conn:
            conn.rollback()
        return 2
    finally:
        if conn:
            conn.close()

    print("Saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
