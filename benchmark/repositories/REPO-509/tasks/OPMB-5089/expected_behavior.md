# Expected behavior

FineTuneJobIdentity: Keep signed finetunejobidentity issuance in SQLite and reject duplicate job_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
