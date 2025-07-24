"""
Provides functions for retrieving mood entries from the database.
"""


import sqlite3


def get_all_moods(conn: sqlite3.Connection) -> list[tuple]:
    """
    Fetch all mood entries from the database.

    Args:
        conn (sqlite3.Connection): SQLite connection object.

    Returns:
        List[Tuple]: List of all rows from the moods table.
    """

    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            moods.id,
            moods.timestamp,
            moods.mood,
            moods.mood_note,
            GROUP_CONCAT(tags.name) AS tag_list
        FROM moods
        LEFT JOIN mood_tags ON moods.id = mood_tags.mood_id
        LEFT JOIN tags ON tags.id = mood_tags.tag_id
        GROUP BY moods.id
        ORDER BY moods.timestamp DESC
    ''')
    return cursor.fetchall()


def get_moods_by_tag(conn: sqlite3.Connection, tag_name: str) -> list[tuple]:
    """
        Fetch all mood entries associated with a given tag from the database.

        Args:
            conn (sqlite3.Connection): SQLite connection object.
            tag_name (str): Relevant tag name to filter mood entries by

        Returns:
            List[Tuple]: List of all rows from the moods table associated with the given tag.
    """

    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            moods.id,
            moods.timestamp,
            moods.mood,
            moods.mood_note,
            GROUP_CONCAT(tags.name) AS tag_list
        FROM moods
        LEFT JOIN mood_tags ON moods.id = mood_tags.mood_id
        LEFT JOIN tags ON mood_tags.tag_id = tags.id
        WHERE tags.name = ?
        GROUP BY moods.id
        ORDER BY moods.timestamp DESC
    """, (tag_name,))
    return cursor.fetchall()
