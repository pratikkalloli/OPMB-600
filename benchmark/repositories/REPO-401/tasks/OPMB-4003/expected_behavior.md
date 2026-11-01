# Expected behavior

Migrate FarmEquipmentOperatorGrant generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Assigns equipment operation privileges by machine class and qualification expiry; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid farm equipment operator grant operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
