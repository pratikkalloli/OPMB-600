# Expected behavior

Migrate SensorCalibrationChain recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Links sensor calibration certificates and correction factors to the device measurement stream; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid sensor calibration chain operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
