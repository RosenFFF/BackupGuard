# Architecture

BackupGuard relies on several core architectural concepts:

1. **Atomic Manifest Writing**: Writes are performed to a temporary file before being moved to the final destination to prevent corruption during generation.
2. **Streaming SHA-256 Hashing**: Files are read in chunks to compute hashes without loading entire files into memory.
3. **Path Security Policies**: Strict validation against directory traversal (e.g., `../`) to ensure operations stay within designated boundaries.
4. **Snapshot Diffing Algorithm**: Compare two manifests to accurately determine added, modified, and deleted files.
