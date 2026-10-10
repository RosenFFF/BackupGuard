"""BackupGuard programmatic usage demonstration."""
import tempfile
from pathlib import Path
from backupguard.manifest import create_manifest, save_manifest, load_manifest
from backupguard.verify import verify_backup
from backupguard.restore import plan_restore

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        source = root / "data"
        source.mkdir()
        (source / "report.csv").write_text("id,val\n1,100\n2,200\n")
        (source / "notes.txt").write_text("backup notes")

        manifest_path = root / "snapshot.json"

        print("1. Creating snapshot manifest...")
        manifest = create_manifest(source)
        save_manifest(manifest, manifest_path)
        print(f"Manifest created with {manifest['file_count']} files.")

        print("\n2. Verifying backup copy...")
        loaded = load_manifest(manifest_path)
        res = verify_backup(loaded, source)
        print(f"Verification valid={res['valid']}, matched={len(res['matched'])}")

        print("\n3. Planning dry-run restoration...")
        target = root / "restored"
        plan = plan_restore(loaded, target)
        for item in plan:
            print(f"  Plan: {item['source_path']} -> {item['target_path']}")

if __name__ == "__main__":
    main()
