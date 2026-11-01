# Expected behavior

Migrate RoamingPartnerProfile recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Provisions roaming partner identifiers, permitted services, and effective dates; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid roaming partner profile operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
