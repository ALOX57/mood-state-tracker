# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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