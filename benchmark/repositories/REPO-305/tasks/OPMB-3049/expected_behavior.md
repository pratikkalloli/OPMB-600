# Expected behavior

Migrate DemandResponseEnrollment recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Enrolls a customer resource in a demand-response event with capacity and opt-out bounds; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid demand response enrollment operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
