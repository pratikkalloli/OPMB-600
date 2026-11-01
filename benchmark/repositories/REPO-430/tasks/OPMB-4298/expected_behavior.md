# Expected behavior

The migrated CloudChangeApproval must malformed digest and unknown decision are rejected. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
