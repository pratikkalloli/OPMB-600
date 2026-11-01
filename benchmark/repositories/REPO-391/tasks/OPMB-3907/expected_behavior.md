# Expected behavior

Migrate IrrigationZoneSchedule load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Issues irrigation commands by field zone with water allocation and soil-moisture constraints; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid irrigation zone schedule operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
