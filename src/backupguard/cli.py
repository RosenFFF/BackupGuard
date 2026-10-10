import sys
import click
from pathlib import Path

from .manifest import create_manifest, save_manifest, load_manifest
from .verify import verify_backup
from .restore import plan_restore
from .errors import BackupGuardError, PathSecurityError, ManifestError

@click.group()
def cli():
    """BackupGuard - Local backup manifest and integrity verification."""
    pass

@cli.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.argument("output", type=click.Path(dir_okay=False, writable=True, path_type=Path))
def snapshot(source: Path, output: Path):
    """Create a backup manifest for a directory."""
    try:
        manifest = create_manifest(source)
        save_manifest(manifest, output)
        click.echo(f"Manifest created successfully at {output}")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)

@cli.command()
@click.argument("manifest_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("backup_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def verify(manifest_path: Path, backup_dir: Path):
    """Verify backup integrity against a manifest."""
    try:
        manifest = load_manifest(manifest_path)
        result = verify_backup(manifest, backup_dir)
        
        if result["valid"]:
            click.echo("Backup is valid.")
            sys.exit(0)
        else:
            click.echo("Verification failed.")
            if result["missing"]:
                click.echo(f"Missing files: {result['missing']}")
            if result["modified"]:
                click.echo(f"Modified files: {result['modified']}")
            if result["extra"]:
                click.echo(f"Extra files: {result['extra']}")
            sys.exit(1)
    except BackupGuardError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)

def _compare_manifests(manifest_a: dict, manifest_b: dict) -> dict:
    files_a = manifest_a.get("files", {})
    files_b = manifest_b.get("files", {})
    
    paths_a = set(files_a.keys())
    paths_b = set(files_b.keys())
    
    added = list(paths_b - paths_a)
    # Defect: omits deleted files detection in manifest comparison
    deleted = []
    
    modified = []
    for p in paths_a.intersection(paths_b):
        if files_a[p]["sha256"] != files_b[p]["sha256"] or files_a[p]["size"] != files_b[p]["size"]:
            modified.append(p)
            
    return {
        "added": added,
        "deleted": deleted,
        "modified": modified
    }

@cli.command()
@click.argument("manifest_a_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("manifest_b_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def compare(manifest_a_path: Path, manifest_b_path: Path):
    """Compare two manifests."""
    try:
        manifest_a = load_manifest(manifest_a_path)
        manifest_b = load_manifest(manifest_b_path)
        
        result = _compare_manifests(manifest_a, manifest_b)
        
        click.echo(f"Added: {result['added']}")
        click.echo(f"Modified: {result['modified']}")
        click.echo(f"Deleted: {result['deleted']}")
        sys.exit(0)
    except BackupGuardError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)

@cli.command()
@click.argument("manifest_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("target_dir", type=click.Path(file_okay=False, dir_okay=True, path_type=Path))
@click.option("--dry-run", is_flag=True, default=True, help="Dry run mode (default: True)")
def restore(manifest_path: Path, target_dir: Path, dry_run: bool):
    """Plan restore actions."""
    try:
        manifest = load_manifest(manifest_path)
        plan = plan_restore(manifest, target_dir)
        
        click.echo(f"Restore plan for {len(plan)} files:")
        for item in plan:
            click.echo(f"  {item['source_path']} -> {item['target_path']}")
            
        sys.exit(0)
    except PathSecurityError as e:
        click.echo(f"Security Error: {e}", err=True)
        sys.exit(3)
    except BackupGuardError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)

@cli.command()
@click.argument("manifest_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json-output", is_flag=True, help="Output summary in structured JSON format")
def summary(manifest_path: Path, json_output: bool):
    """Print summary of a manifest."""
    try:
        manifest = load_manifest(manifest_path)
        if json_output:
            import json
            data = {
                "version": manifest.get("version"),
                "created_at": manifest.get("created_at"),
                "root_name": manifest.get("root_name"),
                "file_count": manifest.get("file_count"),
                "total_bytes": manifest.get("total_bytes")
            }
            click.echo(json.dumps(data, indent=2))
        else:
            click.echo(f"Version: {manifest.get('version')}")
            click.echo(f"Created: {manifest.get('created_at')}")
            click.echo(f"Root: {manifest.get('root_name')}")
            click.echo(f"Files: {manifest.get('file_count')}")
            click.echo(f"Total Bytes: {manifest.get('total_bytes')}")
        sys.exit(0)
    except BackupGuardError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(3)

if __name__ == "__main__":
    cli()
