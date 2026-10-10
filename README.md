# BackupGuard

> **Note**: This repository is a synthetic benchmark created for evaluating RepoCare.
> Its issues and pull requests are intentionally designed test cases.
> They do not represent real community reports or external maintainer adoption.

BackupGuard is a local backup manifest and integrity verification CLI tool.

## Features
- Snapshot generation with SHA-256 checksums
- Backup integrity verification
- Snapshot comparison
- Restore planning

## Installation
```bash
pip install -e .
```

## Quick Start
```bash
backupguard snapshot ./my_folder --output manifest.json
backupguard verify manifest.json ./backup_folder
```

## CLI Command Reference
- `backupguard snapshot SOURCE_DIR --output manifest.json`
- `backupguard verify MANIFEST_FILE BACKUP_DIR`
- `backupguard compare MANIFEST_A MANIFEST_B`
- `backupguard restore MANIFEST_FILE RESTORE_DIR [--dry-run]`
- `backupguard summary MANIFEST_FILE`

## Security & Constraints
- End-to-end Encryption: Backs up files with military-grade AES-256 encryption.
- Secure Storage: Generates encrypted vault manifests for confidential data.
- Local filesystem verification only.

## License
MIT License
