"""
Provides CLI input-handling functions for mood, note, and tags.

Ensures input validation and normalization before storing to the database.
"""


def get_valid_mood_input() -> str:
    """
    Prompt the user to enter a mood rating between 1 and 10.

    Repeats until a valid number within range is provided.

     Returns:
        str: A string representation of the valid mood input value (between "1" and "10").

    """
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
    """
       Prompt the user for an optional mood note.

       Returns:
           str: The user's input, stripped of leading/trailing whitespace.
       """
    return input("Optional note: ").strip()


def get_tags() -> list[str]:
    """
        Prompt the user for optional tags and normalize them.

        Splits the input by commas, strips whitespace, and converts to lowercase.
        Empty or space-only tags are ignored.

        Returns:
            list[str]: A list of the cleaned tag strings.
        """
    raw_tags = input("Enter tags (comma-separated, optional): ")
    if not raw_tags:
        return []
    return [tag.strip().lower() for tag in raw_tags.split(',') if tag.strip()]
