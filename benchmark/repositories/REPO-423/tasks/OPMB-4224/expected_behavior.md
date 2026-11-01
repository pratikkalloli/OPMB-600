# Expected behavior

The migrated BucketManifest must changed object digest is rejected during inventory verification. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
