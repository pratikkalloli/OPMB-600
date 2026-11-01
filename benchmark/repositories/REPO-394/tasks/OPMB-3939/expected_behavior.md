# Expected behavior

Migrate SeedLotProvenance recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records seed lot origin, treatment declarations, and destination planting blocks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid seed lot provenance operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
