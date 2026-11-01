# Expected behavior

The migrated TenantKeyRotation must first key version starts at one for a tenant key lineage. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
