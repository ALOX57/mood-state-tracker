![version](https://img.shields.io/badge/version-0.2.1-blue.svg)

# MoodTracker
A local-first, privacy-preserving mood tracker designed to help users build emotional awareness over time. 
This tool stores mood ratings and optional notes in a secure, offline SQLite database, laying the foundation 
for deeper personal analytics and self-reflection.

---

## Features

- Input a mood rating (1–10) with validation and retry logic
- Optional text note ("mood note") per entry
- Optional tag system
- Automatic timestamping (with timezone awareness)
- Local SQLite database with automatic table creation
- Error logging with stack traces and timestamps
- Clean CLI interface with safe, scalable architecture

## Usage

Run the app from the terminal:
```bash
python main.py
```

You’ll be prompted for:

1. A mood rating (1–10)
2. An optional note (e.g., “feeling tired but focused”)
3. An optional tag input seperated by commas (e.g., tired, sad, focused)
Data is saved to:

```bash
data/logs.db
```

You can view your data using any SQLite browser or query it via Python.

## Versioning

This project uses [Semantic Versioning](https://semver.org/).  
See [CHANGELOG.md](./CHANGELOG.md) for full version history.

**Current version:** `0.2.0`

---

## Roadmap

The project is under active development. Planned upcoming features include:

- Mood trend analytics (weekly/monthly averages)
- Sentiment analysis of notes
- AI/ML pattern detection
- Vector-based note memory
- CLI flags for fast logging and alternate input modes
- Future modular expansion for intelligent self-adaptive systems

---

## Vision

While this begins as a simple mood tracker, the long-term intention is to evolve it into a recursive
self-monitoring system capable of learning from emotional patterns, journaling behavior, and adaptive
feedback. The foundation being built here will support intelligent expansion into areas like mental 
pattern recognition, embedded feedback loops, and ultimately, AI-assisted self-regulation.

This is the seed of something much greater: a system that grows alongside you.
