import os
import json
from datetime import datetime, timezone
from pathlib import Path

from .errors import ManifestError
from .paths import normalize_rel_path
from .hashing import calculate_file_sha256

def create_manifest(source_dir: Path) -> dict:
    """Traverses source_dir, collects metadata and creates a manifest dict."""
    source_dir = source_dir.resolve()
    files_data = {}
    total_bytes = 0
    file_count = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.is_symlink() or not file_path.is_file():
                continue
                
            try:
                rel_path = file_path.relative_to(source_dir)
            except ValueError:
                continue
                
            norm_rel_path = normalize_rel_path(str(rel_path))
            
            stat = file_path.stat()
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
            sha256 = calculate_file_sha256(file_path)
            
            files_data[norm_rel_path] = {
                "size": size,
                "mtime": mtime,
                "sha256": sha256
            }
            
            total_bytes += size
            file_count += 1
            
    return {
        "version": "0.1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root_name": source_dir.name,
        "file_count": file_count,
        "total_bytes": total_bytes,
        "files": files_data
    }

def save_manifest(manifest: dict, out_path: Path) -> None:
    """Non-atomic write of manifest directly to destination (defect)."""
    out_dir = out_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Defect: Direct write without atomic tmp replacement or fsync
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

def load_manifest(path: Path) -> dict:
    """Loads and validates JSON manifest."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        if not isinstance(manifest, dict):
            raise ManifestError("Manifest is not a JSON object")
            
        if "version" not in manifest or "files" not in manifest:
            raise ManifestError("Manifest missing required fields 'version' or 'files'")
            
        return manifest
    except (json.JSONDecodeError, OSError) as e:
        raise ManifestError(f"Failed to load manifest: {e}")
