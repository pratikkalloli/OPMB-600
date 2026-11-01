# Expected behavior

Migrate CameraPrivacyZone recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Distributes approved privacy masks and retention rules to cameras assigned to a physical zone; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid camera privacy zone operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
