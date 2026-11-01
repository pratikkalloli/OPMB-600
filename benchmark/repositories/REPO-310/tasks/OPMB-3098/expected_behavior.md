# Expected behavior

Migrate BatteryDispatchReceipt protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records a storage dispatch request, state-of-charge bounds, and metered response; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid battery dispatch receipt operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
