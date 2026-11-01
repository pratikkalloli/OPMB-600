# Expected behavior

Migrate SensorCalibrationChain verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Links sensor calibration certificates and correction factors to the device measurement stream; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid sensor calibration chain operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
