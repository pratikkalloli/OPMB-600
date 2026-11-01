# Expected behavior

The migrated CloudAuditLedger must duplicate event identifiers are rejected by the database. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
