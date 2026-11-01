# Expected behavior

Migrate FirmwareRolloutRing protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Stages signed firmware releases by device cohort and records promotion or halt decisions; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid firmware rollout ring operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
