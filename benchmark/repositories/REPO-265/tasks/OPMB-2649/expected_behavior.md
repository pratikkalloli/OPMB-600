# Expected behavior

Migrate QualityHoldRelease recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records containment scope and the authorized release decision for material on quality hold; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid quality hold release operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
