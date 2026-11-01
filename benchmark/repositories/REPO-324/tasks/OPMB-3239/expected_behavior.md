# Expected behavior

Migrate CustomerMeterExchange recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Records removal and installation meter serials with final and initial readings; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid customer meter exchange operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
