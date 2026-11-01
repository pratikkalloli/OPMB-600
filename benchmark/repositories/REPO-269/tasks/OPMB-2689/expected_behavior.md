# Expected behavior

Migrate OperatorQualificationGrant recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks operator qualification scope and expiration for safety-sensitive production tasks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid operator qualification grant operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
