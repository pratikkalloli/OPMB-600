# Expected behavior

Migrate GatewayJoinApproval verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Approves a sensor gateway's join request only when its hardware identity and site assignment match; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid gateway join approval operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
