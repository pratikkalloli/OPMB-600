# Expected behavior

The migrated TenantKeyRotation must later versions must advance the stored tenant version. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
