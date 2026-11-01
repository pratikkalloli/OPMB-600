# Expected behavior

Migrate RiverGaugeObservation verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Validates ordered river gauge readings and flags threshold exceedances; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid river gauge observation operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
