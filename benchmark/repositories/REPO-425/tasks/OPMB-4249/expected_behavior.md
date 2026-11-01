# Expected behavior

The migrated TenantKeyRotation must rotation record retrieval preserves signed issuance time. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
