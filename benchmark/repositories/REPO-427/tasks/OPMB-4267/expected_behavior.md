# Expected behavior

The migrated ConfigRollout must promotion requires a signed rollout record for the same environment. Valid signed claims continue to pass; invalid context, modified bytes and wrong keys fail closed.
