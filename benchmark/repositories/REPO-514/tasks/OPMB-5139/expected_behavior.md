# Expected behavior

StreamingLicenseGrant: Keep signed streaminglicensegrant issuance in SQLite and reject duplicate license_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
