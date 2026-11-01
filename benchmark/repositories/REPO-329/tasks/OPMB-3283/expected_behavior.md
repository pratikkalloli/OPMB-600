# Expected behavior

Migrate InverterProtectionProfile generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Approves inverter protection parameters against a connection agreement revision; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid inverter protection profile operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
