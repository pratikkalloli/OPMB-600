# Expected behavior

The migrated WorkloadPassport must malformed passport payload is rejected during decode. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
