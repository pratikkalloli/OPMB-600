# Expected behavior

Migrate BatteryHealthLog apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Captures battery cycle measurements and maintenance decisions for a battery-backed field device; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid battery health log operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
