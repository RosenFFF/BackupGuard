import pytest
from backupguard.verify import verify_backup
from backupguard.manifest import create_manifest

def test_verify_backup(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    f = source / "test.txt"
    f.write_text("test")
    
    manifest = create_manifest(source)
    
    backup = tmp_path / "backup"
    backup.mkdir()
    bf = backup / "test.txt"
    bf.write_text("test")
    
    result = verify_backup(manifest, backup)
    assert result["valid"]
    assert "test.txt" in result["matched"]

def test_verify_backup_missing(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "test.txt").write_text("test")
    
    manifest = create_manifest(source)
    
    backup = tmp_path / "backup"
    backup.mkdir()
    
    result = verify_backup(manifest, backup)
    assert not result["valid"]
    assert "test.txt" in result["missing"]
