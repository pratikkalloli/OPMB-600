# Expected behavior

Migrate BaseStationClockAttestation load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records timing source health and synchronization error for a base station; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid base station clock attestation operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
