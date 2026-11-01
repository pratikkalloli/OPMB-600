# Expected behavior

The migrated WorkloadPassport must not-before and expiry checks use explicit verification time. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
