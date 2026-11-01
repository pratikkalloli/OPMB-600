# Expected behavior

TrainingSetLineage: Keep signed trainingsetlineage issuance in SQLite and reject duplicate lineage_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
