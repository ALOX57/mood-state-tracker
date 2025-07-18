# main.py

from datetime import datetime
import json
import os
import shutil

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

shutil.move(TEMP_FILE, DATA_FILE)


print("Saved.")