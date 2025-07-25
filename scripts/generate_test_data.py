import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from moodtracker.db import init_db, insert_mood
from config import DB_PATH
from datetime import datetime, timedelta
import random


MOOD_PROFILES = {
    "great": {
        "score_range": (8, 10),
        "notes": [
            "Feeling on top of the world.",
            "Crushed the gym today!",
            "Life is really working for me."
        ],
        "tags": ["energized", "happy", "productive"]
    },
    "good": {
        "score_range": (6, 8),
        "notes": [
            "Pretty solid day.",
            "Got some stuff done.",
            "Chill but nice energy."
        ],
        "tags": ["calm", "focused", "satisfied"]
    },
    "okay": {
        "score_range": (4, 6),
        "notes": [
            "Just a normal day.",
            "Not bad, not amazing.",
            "Going through the motions."
        ],
        "tags": ["neutral", "tired", "meh"]
    },
    "bad": {
        "score_range": (2, 4),
        "notes": [
            "Really not feeling it today.",
            "Brain fog and no motivation.",
            "Dragging myself through the day."
        ],
        "tags": ["tired", "anxious", "down"]
    },
    "terrible": {
        "score_range": (1, 2),
        "notes": [
            "Everything sucks.",
            "Can't stop crying.",
            "Just pain."
        ],
        "tags": ["depressed", "angry", "hopeless"]
    },
}


def random_datetime_within_days(days_back=60) -> str:
    offset = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    dt = datetime.now().astimezone() - offset
    return dt.isoformat()


def generate_fake_moods(n=100):
    conn = init_db(DB_PATH)

    for _ in range(n):
        profile_name = random.choice(list(MOOD_PROFILES.keys()))
        profile = MOOD_PROFILES[profile_name]

        mood = str(random.randint(*profile["score_range"]))
        if random.random() < 0.2:
            note = None
        else:
            note = random.choice(profile["notes"])
        tag_count = random.randint(0, len(profile["tags"]))
        tags = random.sample(profile["tags"], tag_count)
        timestamp = random_datetime_within_days()

        insert_mood(conn, timestamp, mood, note, tags)

    conn.commit()
    conn.close()
    print(f"Inserted {n} fake mood entries")


if __name__ == "__main__":
    generate_fake_moods(150)