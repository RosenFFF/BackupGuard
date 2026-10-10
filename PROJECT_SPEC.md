# BackupGuard Project Specification

## Purpose
Local backup manifest generation and integrity verification CLI tool.

## Core Architecture
- Directory walking
- Chunked SHA-256 calculation
- Atomic manifest serialization
- Snapshot comparison (added/modified/deleted)
- Dry-run restore planner with strict path traversal rejection (`../`)

## Security Boundary
- Does NOT copy real data to external services.
- Does NOT encrypt.
- Does NOT delete source files.
- Restore is strictly dry-run in early releases.
- Operates exclusively on user-specified local directories.

## CLI Commands
- `backupguard snapshot SOURCE_DIR --output manifest.json`
- `backupguard verify MANIFEST_FILE BACKUP_DIR`
- `backupguard compare MANIFEST_A MANIFEST_B`
- `backupguard restore MANIFEST_FILE RESTORE_DIR [--dry-run]`
- `backupguard summary MANIFEST_FILE`

## Exit Codes
- 0 = success
- 1 = verification failure / mismatch
- 2 = CLI/argument error
- 3 = filesystem/IO error

## Non-goals
- Not cloud storage
- Not full disaster recovery automation
- Not encryption or compression
