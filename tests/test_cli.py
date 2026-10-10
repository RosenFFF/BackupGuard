import pytest
from click.testing import CliRunner
from backupguard.cli import cli
import json

def test_cli_summary(tmp_path):
    runner = CliRunner()
    
    m = tmp_path / "manifest.json"
    m.write_text(json.dumps({"version": "0.1.0", "files": {}}))
    
    result = runner.invoke(cli, ["summary", str(m)])
    assert result.exit_code == 0
    assert "Version: 0.1.0" in result.output

def test_cli_summary_json(tmp_path):
    runner = CliRunner()
    m = tmp_path / "manifest.json"
    m.write_text(json.dumps({"version": "0.1.0", "files": {}, "file_count": 0, "total_bytes": 0}))
    
    result = runner.invoke(cli, ["summary", str(m), "--json-output"])
    assert result.exit_code == 0
    assert '"version": "0.1.0"' in result.output
    assert '"file_count": 0' in result.output

def test_cli_snapshot_and_verify(tmp_path):
    runner = CliRunner()
    src = tmp_path / "source"
    src.mkdir()
    (src / "file.txt").write_text("hello backup")
    
    manifest_file = tmp_path / "manifest.json"
    res_snap = runner.invoke(cli, ["snapshot", str(src), str(manifest_file)])
    assert res_snap.exit_code == 0
    assert manifest_file.exists()
    
    res_ver = runner.invoke(cli, ["verify", str(manifest_file), str(src)])
    assert res_ver.exit_code == 0
    assert "Backup is valid" in res_ver.output

def test_cli_compare(tmp_path):
    runner = CliRunner()
    m1 = tmp_path / "m1.json"
    m2 = tmp_path / "m2.json"
    m1.write_text(json.dumps({"version": "0.1.0", "files": {"a.txt": {"size": 1, "sha256": "111", "mtime": ""}}}))
    m2.write_text(json.dumps({"version": "0.1.0", "files": {"b.txt": {"size": 2, "sha256": "222", "mtime": ""}}}))
    
    res = runner.invoke(cli, ["compare", str(m1), str(m2)])
    assert res.exit_code == 0
    assert "Added: ['b.txt']" in res.output

def test_cli_restore(tmp_path):
    runner = CliRunner()
    m = tmp_path / "manifest.json"
    m.write_text(json.dumps({"version": "0.1.0", "files": {"doc.txt": {"size": 4, "sha256": "aaa", "mtime": ""}}}))
    target = tmp_path / "restore_dir"
    
    res = runner.invoke(cli, ["restore", str(m), str(target), "--dry-run"])
    assert res.exit_code == 0
    assert "Restore plan for 1 files" in res.output
