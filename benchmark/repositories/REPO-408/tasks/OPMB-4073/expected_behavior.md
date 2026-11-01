# Expected behavior

Migrate AirQualitySensorEvidence generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Preserves air sensor calibration and pollutant interval evidence for an observation site; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid air quality sensor evidence operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
