# Expected behavior

Migrate TransitOperatorCredential load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Assigns route and vehicle qualifications to a transit operator for a bounded duty period; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid transit operator credential operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
