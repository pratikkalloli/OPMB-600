# Expected behavior

Migrate ConsumableShelfLifeCard protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks lot expiry and opened-container life for process consumables used by a production cell; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid consumable shelf life card operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
