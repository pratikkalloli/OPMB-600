# Expected behavior

APIClientEnrollment: Keep signed apiclientenrollment issuance in SQLite and reject duplicate client_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
