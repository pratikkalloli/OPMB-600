# Expected behavior

Migrate EmbeddedConfigBundle recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Approves a device-specific configuration bundle with a monotonic revision and rollback policy; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid embedded config bundle operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
