# Expected behavior

ModelRollbackPermit: Keep signed modelrollbackpermit issuance in SQLite and reject duplicate permit_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
