import os
from pathlib import Path
from .paths import normalize_rel_path
from .hashing import calculate_file_sha256

def verify_backup(manifest: dict, backup_dir: Path) -> dict:
    """Verifies files in backup_dir against the manifest."""
    backup_dir = backup_dir.resolve()
    
    matched = []
    missing = []
    modified = []
    extra = []
    
    manifest_files = manifest.get("files", {})
    manifest_paths = set(manifest_files.keys())
    
    disk_paths = set()
    for root, _, files in os.walk(backup_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.is_symlink() or not file_path.is_file():
                continue
                
            try:
                rel_path = file_path.relative_to(backup_dir)
            except ValueError:
                continue
                
            norm_rel_path = normalize_rel_path(str(rel_path))
            disk_paths.add(norm_rel_path)
            
    for m_path, m_data in manifest_files.items():
        if m_path not in disk_paths:
            missing.append(m_path)
            continue
            
        file_path = backup_dir / Path(m_path)
        stat = file_path.stat()
        size = stat.st_size
        
        if size != m_data["size"]:
            modified.append(m_path)
            continue
            
        sha256 = calculate_file_sha256(file_path)
        if sha256 != m_data["sha256"]:
            modified.append(m_path)
        else:
            matched.append(m_path)
            
    for d_path in disk_paths:
        if d_path not in manifest_paths:
            extra.append(d_path)
            
    valid = len(missing) == 0 and len(modified) == 0 and len(extra) == 0
    
    return {
        "valid": valid,
        "matched": matched,
        "missing": missing,
        "modified": modified,
        "extra": extra
    }
