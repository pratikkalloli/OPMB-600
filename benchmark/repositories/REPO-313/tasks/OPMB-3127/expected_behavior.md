# Expected behavior

Migrate SubstationRelaySetting load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Controls relay setting revisions, coordination review, and staged commissioning; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid substation relay setting operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
