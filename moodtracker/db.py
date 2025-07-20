import sqlite3

def init_db(path: str) -> sqlite3.Connection:
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
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, mood, mood_note)
        VALUES (?, ?, ?)
    ''', (timestamp, mood, note))
    mood_id = cursor.lastrowid

    for tag_name in tags:
        tag_name = tag_name.strip().lower()

        # Check if tag exists
        cursor.execute('SELECT id FROM tags WHERE name = ?', tag_name)
        result = cursor.fetchone()

        if result:
            tag_id = result[0]
        else:
            # Insert new tag
            cursor.execute('INSERT INTO tags (name) VALUES (?)', tag_name)
            tag_id = cursor.lastrowid

        # Link mood and tag in join table
        cursor.execute('INSERT INTO mood_tags (mood_id, tag_id) VALUES (?, ?)', (mood_id, tag_id))

    conn.commit()
