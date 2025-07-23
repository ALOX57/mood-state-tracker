# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [0.2.2] - 2025-07-23
### Added
- Unit test for error logging utility using monkeypatching.
- Two additional database tests:
  - Handling whitespace-only tags.
  - Shared tag behavior across multiple mood entries.
- Full function-level docstrings for all test modules and core classes.


## [0.2.1] - 2025-07-20
### Fixed
- Case-insensitive tag duplication: Tags like "Happy" and "happy" now correctly resolve to a single tag entry.

### Added
- Unit tests for `insert_mood`:
  - Handles mood insertion with/without notes and tags
  - Validates correct tag linking
  - Ensures tag deduplication and case normalization
- Unit tests for `get_tags` input parsing logic


## [0.2.0] - 2025-07-20
### Added
- Tag system: users can now enter tags per mood
- Tags are stored in separate table and linked to moods
- CLI input for comma-separated tags

### Fixed
- Error when passing single tag string (tuple binding issue)
- Logger path now correctly uses config value

## [0.1.1] - 2025-07-19

### Changed
- Refactored project structure into modular packages
- Moved config, logger, database logic into separate files
- Updated import paths and project layout

## [0.1.0] - 2025-07-19

### Added

- Initial mood tracking system using SQLite
- User input for mood (1–10) with validation
- Error logging with timestamped logs
- Local database setup with automatic table creation
- `mood_note` input (optional) stored with mood and timestamp
- Looping mood input to ensure valid entry