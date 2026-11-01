# Expected behavior

CertificatePinRollout: Keep signed certificatepinrollout issuance in SQLite and reject duplicate rollout_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
