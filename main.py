# main.py

from datetime import datetime
import sqlite3

print(datetime.now().isoformat())

def validate_mood(raw):
    raw = raw.strip()
    if raw.isDigit():
        val = int(raw)
        if 1 <= val <= 10:
            return str(val)
        else:
            print("Numeric mood must be between 1 and 10.")
            exit()
    elif raw:
        return raw
    else:
        print("Mood cannot be empty.")
        exit()

mood = input("Mood (1-10 or label): ")
mood = validate_mood(mood)




print("You entered:", mood)


entry = {
    "timestamp": datetime.now().isoformat(),
    "mood": mood
}

DB_FILE = 'data/logs.db'

try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        mood TEXT NOT NULL
    )    
    ''')

    cursor.execute('''
    INSERT INTO logs (timestamp, mood)
    VALUES (?, ?)
    ''', (entry["timestamp"], entry["mood"]))

    conn.commit()
except Exception as e:
    print("ERROR: Failed to write to database.")
    print(e)
    conn.rollback()
    exit()
finally:
    conn.close()

print("Saved.")
