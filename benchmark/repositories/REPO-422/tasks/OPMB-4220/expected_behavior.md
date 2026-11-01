# Expected behavior

The migrated WorkloadPassport must rotation to a new issuer key preserves old-key verification policy. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
