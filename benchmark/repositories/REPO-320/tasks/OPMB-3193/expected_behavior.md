# Expected behavior

Migrate WaterPumpEnergyLedger generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Reconciles pump runtime and energy readings against a water delivery schedule; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid water pump energy ledger operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
