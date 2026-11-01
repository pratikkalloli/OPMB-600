# Expected behavior

Migrate WeatherStationCalibration apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records environmental station calibration checks and correction factors; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid weather station calibration operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
