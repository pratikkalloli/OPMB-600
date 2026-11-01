# Expected behavior

Migrate PeeringKeyAgreement recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records partner endpoint identity and key rotation state for a simulated peering link; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid peering key agreement operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
