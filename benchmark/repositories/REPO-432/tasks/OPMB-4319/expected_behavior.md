# Expected behavior

FederatedServiceTrust: Keep signed federated trust issuance in SQLite and reject duplicate trust_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
