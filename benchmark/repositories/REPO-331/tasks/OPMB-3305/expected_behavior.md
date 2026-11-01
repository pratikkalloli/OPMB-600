# Expected behavior

Migrate RailSignalAspectArchive verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Preserves signal aspect transitions with route, interlocking revision, and event sequence; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid rail signal aspect archive operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
