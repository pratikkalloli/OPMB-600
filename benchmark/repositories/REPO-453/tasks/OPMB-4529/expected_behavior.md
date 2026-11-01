# Expected behavior

CIWorkerEnrollment: Keep signed ciworkerenrollment issuance in SQLite and reject duplicate worker_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
