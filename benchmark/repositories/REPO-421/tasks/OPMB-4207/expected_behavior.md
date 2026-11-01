# Expected behavior

The migrated CloudQuotaGrant must expired grant rejection using caller-supplied clock. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
