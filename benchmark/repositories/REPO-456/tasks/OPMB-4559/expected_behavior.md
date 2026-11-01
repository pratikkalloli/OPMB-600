# Expected behavior

SourcePackageAttestation: Keep signed sourcepackageattestation issuance in SQLite and reject duplicate package_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
