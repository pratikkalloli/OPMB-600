# Expected behavior

The migrated TenantKeyRotation must malformed key digest is rejected before persistence. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
