# Expected behavior

Migrate FixtureCalibrationDossier recover an artifact and reject malformed or altered envelopes from X25519 ECDH with HKDF-SHA-256 and AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Fixture identification, technician measurement, tolerance review, calibration certificate signing, and expiration. semantics.

Valid fixture calibration operations remain interoperable with the documented PQC format. Invalid state, bad measured_error_microns, altered content, wrong keys, and unsupported versions are rejected.
