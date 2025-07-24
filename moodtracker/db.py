"""
Handles all database operations for storing mood logs, tags, and their relationships.

Includes functions to initialize the database schema and insert mood entries with optional tags.
"""


from contextlib import contextmanager
from config import DB_PATH
import sqlite3


def init_db(path: str) -> sqlite3.Connection:
    """
    Initialises the SQLite database and creates required tables if they don't exist.

    Args:
        path (str): The path to the SQLite database file.

    Returns:
        sqlite3.Connection: A connection object to the initialised database.

    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            mood TEXT NOT NULL,
            mood_note TEXT
        )    
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE 
        )    
    ''')

    # Joining table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_tags (
            mood_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (mood_id) REFERENCES logs(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        )    
    ''')

    conn.commit()
    return conn


def insert_mood(conn: sqlite3.Connection, timestamp: str, mood: str, note: str, tags: list[str]) -> None:
    """
    Inserts a mood entry into the database and links the associated tags

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
        timestamp (str): The timestamp of the mood entry in ISO 8601 format.
        mood (str): The user's mood value or label.
        note (str): An optional text note explaining the mood entry.
        tags (list[str]): A list of tags to associate with this mood entry.

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, mood, mood_note)
        VALUES (?, ?, ?)
    ''', (timestamp, mood, note))
    mood_id = cursor.lastrowid

    normalized_tags = [tag.strip().lower() for tag in tags if tag.strip()]
    unique_tags = list(dict.fromkeys(normalized_tags))
    for tag_name in unique_tags:
        tag_name = tag_name.strip().lower()

        # Check if tag exists
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        result = cursor.fetchone()

        if result:
            tag_id = result[0]
        else:
            # Insert new tag
            cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
            tag_id = cursor.lastrowid

        # Link mood and tag in join table
        cursor.execute('INSERT INTO mood_tags (mood_id, tag_id) VALUES (?, ?)', (mood_id, tag_id))

    conn.commit()


@contextmanager
def get_connection(path: str = DB_PATH):
    """
    Context manager for the SQLite connection.

    Args:
        path (str): Path to the SQLite database.

    Yields:
        sqlite3.Connection: Open connection to the database.

    Ensures the connection is closed automatically when the block exits, even if an error occurs.
    """

    conn = init_db(path)
    try:
        yield conn
    finally:
        conn.close()
