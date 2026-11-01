# Expected behavior

Migrate RiverGaugeObservation recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Validates ordered river gauge readings and flags threshold exceedances; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid river gauge observation operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
