# Expected behavior

Migrate IoTDataRetentionPolicy apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Assigns retention and deletion schedules to device data classes with an auditable policy revision; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid io t data retention policy operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
