# Expected behavior

Migrate TrainConsistRevision generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Versions train consist order and checks vehicle compatibility before departure; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid train consist revision operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
