# Expected behavior

Migrate FarmEquipmentOperatorGrant protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Assigns equipment operation privileges by machine class and qualification expiry; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid farm equipment operator grant operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
