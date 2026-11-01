# Expected behavior

Migrate FixtureCalibrationDossier load and validate a serialized verification key from ECDSA P-256/SHA-256 to ML-DSA-65, retaining Fixture identification, technician measurement, tolerance review, calibration certificate signing, and expiration. semantics.

Valid fixture calibration operations remain interoperable with the documented PQC format. Invalid state, bad measured_error_microns, altered content, wrong keys, and unsupported versions are rejected.
