# Expected behavior

The migrated WorkloadPassport must signing preserves not-before and expiry boundaries. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
