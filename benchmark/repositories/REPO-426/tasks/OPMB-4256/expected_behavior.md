# Expected behavior

The migrated CloudAuditLedger must sequence continuity is verified when reading the ledger. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
