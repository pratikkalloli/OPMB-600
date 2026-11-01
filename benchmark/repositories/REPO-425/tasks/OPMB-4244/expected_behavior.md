# Expected behavior

The migrated TenantKeyRotation must modified key digest invalidates the transition signature. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
