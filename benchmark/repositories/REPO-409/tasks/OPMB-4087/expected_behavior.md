# Expected behavior

Migrate FertilizerBlendTicket load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records fertilizer blend proportions and field allocation against nutrient limits; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid fertilizer blend ticket operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
