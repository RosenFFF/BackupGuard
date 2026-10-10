import pytest
from backupguard.errors import (
    BackupGuardError,
    ManifestError,
    PathSecurityError,
    VerificationError,
    HashMismatchError,
)

def test_custom_exception_hierarchy():
    for exc_cls in [
        ManifestError,
        PathSecurityError,
        VerificationError,
        HashMismatchError,
    ]:
        exc = exc_cls("sample message")
        assert isinstance(exc, BackupGuardError)
        assert str(exc) == "sample message"
