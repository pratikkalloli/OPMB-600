# Expected behavior

The migrated SaaSExportPermit must export check rejects a requester mismatch. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
