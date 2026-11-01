# Expected behavior

Migrate ConsumableShelfLifeCard apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks lot expiry and opened-container life for process consumables used by a production cell; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid consumable shelf life card operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
