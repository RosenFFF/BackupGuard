import pytest
from backupguard.restore import plan_restore
from backupguard.errors import PathSecurityError

def test_plan_restore(tmp_path):
    manifest = {
        "files": {
            "a.txt": {"size": 1, "sha256": "a"}
        }
    }
    
    target = tmp_path / "target"
    target.mkdir()
    
    plan = plan_restore(manifest, target)
    assert len(plan) == 1
    assert plan[0]["source_path"] == "a.txt"
    assert plan[0]["target_path"] == str((target / "a.txt").resolve())

def test_plan_restore_unsafe(tmp_path):
    manifest = {
        "files": {
            "../a.txt": {"size": 1, "sha256": "a"}
        }
    }
    
    target = tmp_path / "target"
    target.mkdir()
    
    with pytest.raises(PathSecurityError):
        plan_restore(manifest, target)
