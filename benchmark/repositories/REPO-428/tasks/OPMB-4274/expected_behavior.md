# Expected behavior

The migrated BackupReceipt must changed root digest is rejected before restore authorization. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
