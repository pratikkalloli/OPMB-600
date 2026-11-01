# Expected behavior

Migrate FirmwareRollbackPermit protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Approves a rollback to a previously signed firmware revision after a defined failure trigger; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid firmware rollback permit operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
