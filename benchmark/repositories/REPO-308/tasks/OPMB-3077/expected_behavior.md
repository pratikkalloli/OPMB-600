# Expected behavior

Migrate TurbineMaintenanceDossier load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records wind turbine maintenance work, component serials, and post-service inspection; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid turbine maintenance dossier operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
