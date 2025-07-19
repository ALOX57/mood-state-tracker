# main.py

from datetime import datetime
import json
import os
import shutil
import sqlite3

print(datetime.now().isoformat())

mood = input("Mood (1-10 or label): ").strip()
print("You entered:", mood)

DATA_FILE = 'data/logs.json'

entry = {
    "timestamp": datetime.now().isoformat(),
    "mood": mood
}


# Load existing logs - or empty list if file is new/broken
if not os.path.exists(DATA_FILE):
    logs = []
else:
    with open(DATA_FILE, 'r') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

logs.append(entry)

# with open(DATA_FILE, 'w') as f:
#     json.dump(logs, f, indent=2)

# Writing to temp file
TEMP_FILE = 'data/logs_temp.json'

with open(TEMP_FILE, 'w') as f:
    json.dump(logs, f, indent=2)
    f.flush()
    os.fsync(f.fileno())

# Validate
with open(TEMP_FILE, 'r') as f:
    try:
        test = json.load(f)
        assert isinstance(test, list)
        for item in test:
            assert isinstance(item, dict)
            assert "mood" in item
            assert "timestamp" in item
    except Exception:
        print("ERROR: Temp file corrupted - not replacing original!")
        exit()
shutil.move(TEMP_FILE, DATA_FILE)


print("Saved.")




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
