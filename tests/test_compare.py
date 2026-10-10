import pytest
from backupguard.cli import _compare_manifests

def test_compare_manifests():
    a = {
        "files": {
            "1.txt": {"size": 1, "sha256": "1"},
            "2.txt": {"size": 2, "sha256": "2"}
        }
    }
    b = {
        "files": {
            "2.txt": {"size": 2, "sha256": "3"},
            "3.txt": {"size": 3, "sha256": "3"}
        }
    }
    
    res = _compare_manifests(a, b)
    assert set(res["added"]) == {"3.txt"}
    assert set(res["deleted"]) == {"1.txt"}
    assert set(res["modified"]) == {"2.txt"}
