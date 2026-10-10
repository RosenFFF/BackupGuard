import pytest
from pathlib import Path
from backupguard.paths import normalize_rel_path, is_safe_relative_path, resolve_within_root
from backupguard.errors import PathSecurityError

def test_normalize_rel_path():
    assert normalize_rel_path("a\\b/c") == "a/b/c"
    assert normalize_rel_path("a//b") == "a/b"
    assert normalize_rel_path("/a/") == "a"

def test_is_safe_relative_path():
    assert is_safe_relative_path("a/b")
    assert not is_safe_relative_path("/a/b")
    assert not is_safe_relative_path("C:/a")
    assert not is_safe_relative_path("../a")
    assert not is_safe_relative_path("a/../b")

def test_resolve_within_root(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    
    safe_target = resolve_within_root(root, "a/b")
    assert safe_target == root / "a" / "b"
    
    with pytest.raises(PathSecurityError):
        resolve_within_root(root, "../a")
