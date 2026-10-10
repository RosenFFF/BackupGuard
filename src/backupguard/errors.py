class BackupGuardError(Exception):
    """Base class for BackupGuard errors."""
    pass

class ManifestError(BackupGuardError):
    """Raised when there is an error reading or parsing the manifest."""
    pass

class PathSecurityError(BackupGuardError):
    """Raised when a path is unsafe or attempts path traversal."""
    pass

class VerificationError(BackupGuardError):
    """Raised during verification failures (though verification mostly returns dicts)."""
    pass

class HashMismatchError(BackupGuardError):
    """Raised when a hash mismatch occurs."""
    pass
