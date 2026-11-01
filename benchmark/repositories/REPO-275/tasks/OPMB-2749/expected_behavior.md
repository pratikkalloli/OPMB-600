# Expected behavior

Migrate GatewayJoinApproval recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Approves a sensor gateway's join request only when its hardware identity and site assignment match; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid gateway join approval operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
