import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from moodtracker.db import init_db, insert_mood
from config import DB_PATH
from datetime import datetime, timedelta
import random
import argparse


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

PERSONA_PROFILES = {
    "HappyUser": {
        "weights": {
            "great": 0.4,
            "good": 0.35,
            "okay": 0.2,
            "bad": 0.05,
            "terrible": 0.0
        }
    },
    "DepressedUser": {
        "weights": {
            "great": 0.02,
            "good": 0.08,
            "okay": 0.2,
            "bad": 0.35,
            "terrible": 0.35
        }
    }
}


def random_datetime_within_days(days_back=60) -> str:
    offset = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    dt = datetime.now().astimezone() - offset
    return dt.isoformat()


def generate_fake_moods(n=100, persona=None, clear_existing=False):
    conn = init_db(DB_PATH)

    if clear_existing:
        clear_all_mood_data(conn)

    for _ in range(n):
        if persona in PERSONA_PROFILES:
            weights = PERSONA_PROFILES[persona]["weights"]
            profile_name = random.choices(
                population=list(weights.keys()),
                weights=list(weights.values()),
                k=1
            )[0]
        else:
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


def clear_all_mood_data(conn):
    conn.execute("DELETE FROM moods")
    conn.commit()
    print("Cleared existing mood entries")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake mood data")
    parser.add_argument("--n", type=int, default=150, help="Number of entries to generate")
    parser.add_argument("--persona", type=str, default=None, help="Persona to simulate")
    parser.add_argument("--clear", action="store_true", help="Clear old data before inserting new entries")

    args = parser.parse_args()
    generate_fake_moods(n=args.n, persona=args.persona, clear_existing=args.clear)
