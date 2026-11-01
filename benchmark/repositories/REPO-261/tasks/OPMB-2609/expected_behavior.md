# Expected behavior

Migrate MachineGuardInspection recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records machine-guard inspection findings and prevents restart until safety-critical findings are closed; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid machine guard inspection operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
