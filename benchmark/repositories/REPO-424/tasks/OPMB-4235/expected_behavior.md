# Expected behavior

The migrated MeshServiceLease must lease renewal increments service sequence monotonically. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
