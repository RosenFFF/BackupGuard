import pytest
import json
from pathlib import Path
from backupguard.manifest import create_manifest, save_manifest, load_manifest
from backupguard.errors import ManifestError

def test_create_manifest(tmp_path):
    d = tmp_path / "source"
    d.mkdir()
    (d / "a.txt").write_text("a")
    (d / "b.txt").write_text("b")
    
    manifest = create_manifest(d)
    assert manifest["file_count"] == 2
    assert "a.txt" in manifest["files"]
    assert "b.txt" in manifest["files"]

def test_save_load_manifest(tmp_path):
    manifest = {"version": "0.1.0", "files": {}}
    out = tmp_path / "manifest.json"
    
    save_manifest(manifest, out)
    assert out.exists()
    
    loaded = load_manifest(out)
    assert loaded == manifest

def test_load_manifest_invalid(tmp_path):
    out = tmp_path / "invalid.json"
    out.write_text("not json")
    
    with pytest.raises(ManifestError):
        load_manifest(out)
