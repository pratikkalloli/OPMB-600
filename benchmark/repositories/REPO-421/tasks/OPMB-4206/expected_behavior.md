# Expected behavior

The migrated CloudQuotaGrant must authorization rejects requests exceeding the signed ceiling. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
