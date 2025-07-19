# main.py

from datetime import datetime
import sqlite3

print(datetime.now().isoformat())

mood = input("Mood (1-10 or label): ").strip()
print("You entered:", mood)


entry = {
    "timestamp": datetime.now().isoformat(),
    "mood": mood
}

DB_FILE = 'data/logs.db'
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
conn.close()

print("Saved.")
