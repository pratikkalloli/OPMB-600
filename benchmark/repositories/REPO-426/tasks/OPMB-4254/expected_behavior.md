# Expected behavior

The migrated CloudAuditLedger must tampered previous hash breaks signature validation. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
