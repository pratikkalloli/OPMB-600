# Expected behavior

Migrate OperatorQualificationGrant load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks operator qualification scope and expiration for safety-sensitive production tasks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid operator qualification grant operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
