# Expected behavior

Migrate BaseStationClockAttestation protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records timing source health and synchronization error for a base station; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid base station clock attestation operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
