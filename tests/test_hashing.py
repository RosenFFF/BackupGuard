import pytest
import hashlib
from backupguard.hashing import calculate_file_sha256

def test_calculate_file_sha256(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("test")
    
    expected = hashlib.sha256(b"test").hexdigest()
    assert calculate_file_sha256(f) == expected

def test_calculate_file_sha256_empty(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_bytes(b"")
    
    expected = hashlib.sha256(b"").hexdigest()
    assert calculate_file_sha256(f) == expected
