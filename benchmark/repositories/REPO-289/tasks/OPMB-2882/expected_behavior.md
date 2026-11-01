# Expected behavior

Migrate SensorBatchProvenance canonicalize the complete domain record for signing from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records production lot, calibration status, and destination for a batch of deployed sensors; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid sensor batch provenance operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
