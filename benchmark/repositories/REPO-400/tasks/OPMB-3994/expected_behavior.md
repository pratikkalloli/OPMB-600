# Expected behavior

Migrate BeehiveHealthObservation sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks synthetic hive health observations, inspection evidence, and intervention status; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid beehive health observation operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
