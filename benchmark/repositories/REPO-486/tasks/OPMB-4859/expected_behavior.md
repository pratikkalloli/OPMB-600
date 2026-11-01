# Expected behavior

ExperimentNotebookSeal: Keep signed experimentnotebookseal issuance in SQLite and reject duplicate notebook_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
