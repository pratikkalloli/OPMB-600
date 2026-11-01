# Expected behavior

SBOMPublicationGate: Keep signed sbompublicationgate issuance in SQLite and reject duplicate gate_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
