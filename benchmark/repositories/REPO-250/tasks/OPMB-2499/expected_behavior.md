# Expected behavior

Migrate ComponentTraceLot recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Receiving inspection, source-lot binding, production consumption, and traceability export. semantics.

Valid component trace operations remain interoperable with the documented PQC format. Invalid state, bad material_digest, altered content, wrong keys, and unsupported versions are rejected.
