# Expected behavior

The migrated TenantKeyRotation must verification rejects records for a different tenant. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
