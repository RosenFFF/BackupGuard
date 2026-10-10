import hashlib
from pathlib import Path

def calculate_file_sha256(filepath: Path, chunk_size: int = 65536) -> str:
    """Streams file in chunks to calculate SHA-256."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
