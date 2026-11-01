# Expected behavior

The migrated CloudQuotaGrant must duplicate grant identifiers are rejected by persistence. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
