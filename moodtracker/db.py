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


def insert_mood(conn: sqlite3.Connection, timestamp: str, mood: str, note: str) -> None:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, mood, mood_note)
        VALUES (?, ?, ?)
    ''', (timestamp, mood, note))
    conn.commit()
