# Expected behavior

Migrate ToolChangeAuthorization recover an artifact and reject malformed or altered envelopes from X25519 ECDH with HKDF-SHA-256 and AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tool wear report, technician assignment, supervisor authorization, change confirmation, and return-to-service. semantics.

Valid tool change operations remain interoperable with the documented PQC format. Invalid state, bad tool_serial, altered content, wrong keys, and unsupported versions are rejected.
