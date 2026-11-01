# Expected behavior

Migrate FleetCertificateRotation serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Rotates device fleet certificates in cohorts and tracks overlap and retirement windows; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid fleet certificate rotation operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
