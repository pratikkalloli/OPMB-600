# Expected behavior

The migrated CloudQuotaGrant must verification rejects grant mutation and wrong issuer. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
