# Expected behavior

The migrated BucketManifest must duplicate object names are rejected before signing. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
