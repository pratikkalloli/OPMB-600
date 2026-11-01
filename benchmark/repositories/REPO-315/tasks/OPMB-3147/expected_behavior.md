# Expected behavior

Migrate EVChargeSession load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records a charging session's meter start/end, station identity, and settlement state; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid e v charge session operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
