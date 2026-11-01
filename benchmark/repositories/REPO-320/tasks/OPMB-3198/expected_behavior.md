# Expected behavior

Migrate WaterPumpEnergyLedger protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Reconciles pump runtime and energy readings against a water delivery schedule; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid water pump energy ledger operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
