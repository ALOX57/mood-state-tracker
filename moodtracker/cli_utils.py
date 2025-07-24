"""CLI output formatting helpers."""

from moodtracker.utils import format_timestamp


def display_moods(entries: list, header: str) -> None:
    """Print a list of mood rows with a header."""
    print(f"\n=== {header} ===")
    for _, iso_ts, score, note, tag_str in entries:
        # Convert ISO string to datetime object and format for readability
        formatted_ts = format_timestamp(iso_ts)
        tag_display = f"Tags: {tag_str}" if tag_str else "Tags: (none)"
        print(f"[{formatted_ts}] Mood: {score}  {tag_display}  Note: {note or '(none)'}")
