# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-10-10
### Added
- Added `--json-output` option to `backupguard summary` for automated pipeline integration.
- Expanded CLI test coverage for JSON format inspection.

## [0.1.0] - 2026-10-10
### Added
- Directory manifest generation with atomic temporary write replacement.
- Chunked streaming SHA-256 calculation for large files.
- Backup integrity verification against snapshots (matched/missing/modified/extra).
- Snapshot diffing (added/modified/deleted).
- Dry-run restoration planner with strict path traversal prevention.
- Command-line interface with Click.
