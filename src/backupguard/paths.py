import os
import re
from pathlib import Path
from .errors import PathSecurityError

def normalize_rel_path(path_str: str) -> str:
    """Normalizes relative path using forward slashes / across OS platforms."""
    # Convert backslashes to forward slashes
    path = path_str.replace("\\", "/")
    # Remove redundant slashes
    path = re.sub(r'/+', '/', path)
    return path.strip("/")

def is_safe_relative_path(rel_path: str) -> bool:
    """Returns False if path starts with /, \\, drive letter, or contains .. components."""
    if not rel_path:
        return True
    
    # Check for absolute paths (starts with / or \)
    if rel_path.startswith("/") or rel_path.startswith("\\"):
        return False
        
    # Check for drive letters (Windows) e.g., C: D: C:\
    if re.match(r'^[a-zA-Z]:', rel_path):
        return False
        
    # Check for .. components
    normalized = normalize_rel_path(rel_path)
    parts = normalized.split("/")
    if ".." in parts:
        return False
        
    return True

def resolve_within_root(root: Path, rel_path: str) -> Path:
    """Strictly resolves target path inside root, raising PathSecurityError if it escapes root."""
    if not is_safe_relative_path(rel_path):
        raise PathSecurityError(f"Path is unsafe: {rel_path}")
        
    root_resolved = root.resolve()
    # Normalize rel_path for joining
    rel_path_norm = normalize_rel_path(rel_path)
    target_path = root_resolved.joinpath(rel_path_norm).resolve()
    
    try:
        target_path.relative_to(root_resolved)
    except ValueError:
        raise PathSecurityError(f"Path escapes root directory: {rel_path}")
        
    return target_path
