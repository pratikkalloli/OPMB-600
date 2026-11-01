# Expected behavior

Migrate EVChargeSession recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records a charging session's meter start/end, station identity, and settlement state; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid e v charge session operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
