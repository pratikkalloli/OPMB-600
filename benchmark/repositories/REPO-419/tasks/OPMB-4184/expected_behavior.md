# Expected behavior

Migrate ReservoirWaterQuality sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Seals reservoir water quality measurements and threshold-based response decisions; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid reservoir water quality operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
