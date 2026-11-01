# Expected behavior

The migrated CloudQuotaGrant must audit record preserves the exact signed quota context. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
