# Expected behavior

Migrate RenewableOutputCertificate recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Attests renewable generator output for a defined meter interval and plant identity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid renewable output certificate operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
