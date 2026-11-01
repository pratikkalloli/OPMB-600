# Expected behavior

Migrate SoilProbeCalibration load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks soil probe calibration factors and service interval for a named field location; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid soil probe calibration operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
