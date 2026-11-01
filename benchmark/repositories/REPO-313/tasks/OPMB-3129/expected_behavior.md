# Expected behavior

Migrate SubstationRelaySetting recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Controls relay setting revisions, coordination review, and staged commissioning; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid substation relay setting operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
