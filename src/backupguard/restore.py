from pathlib import Path
from typing import List, Dict, Any
from .paths import is_safe_relative_path, resolve_within_root
from .errors import PathSecurityError

def plan_restore(manifest: dict, target_dir: Path) -> List[Dict[str, Any]]:
    """Plans restoration actions, validating paths to prevent path traversal."""
    plan = []
    target_dir = target_dir.resolve()
    
    files = manifest.get("files", {})
    
    for rel_path, data in files.items():
        if not is_safe_relative_path(rel_path):
            raise PathSecurityError(f"Unsafe path in manifest: {rel_path}")
            
        # This will raise PathSecurityError if it escapes root
        target_path = resolve_within_root(target_dir, rel_path)
        
        plan.append({
            "source_path": rel_path,
            "target_path": str(target_path),
            "size": data.get("size", 0),
            "sha256": data.get("sha256", "")
        })
        
    return plan
