def get_valid_mood_input() -> str:
    while True:
        raw = input("Mood (1-10): ").strip()
        if not raw:
            print("Mood cannot be empty.")
            continue
        if raw.isdigit():
            val = int(raw)
            if 1 <= val <= 10:
                return str(val)
            else:
                print("Mood must be between 1 and 10.")
        else:
            print("Mood must be a number between 1 and 10.")

def get_optional_note() -> str:
    return input("Optional note: ").strip()