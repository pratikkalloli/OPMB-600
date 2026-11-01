# Expected behavior

The migrated TenantKeyRotation must signed transition binds the new public-key digest. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
