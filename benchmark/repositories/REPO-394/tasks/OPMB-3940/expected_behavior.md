# Expected behavior

Migrate SeedLotProvenance apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records seed lot origin, treatment declarations, and destination planting blocks; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid seed lot provenance operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
