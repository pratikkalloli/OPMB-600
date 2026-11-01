# Expected behavior

LabelingBatchProvenance: Keep signed labelingbatchprovenance issuance in SQLite and reject duplicate batch_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
