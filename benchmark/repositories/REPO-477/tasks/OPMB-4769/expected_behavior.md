# Expected behavior

BuildGraphSignature: Keep signed buildgraphsignature issuance in SQLite and reject duplicate graph_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
