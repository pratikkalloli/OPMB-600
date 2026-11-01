# Expected behavior

Migrate FirmwareRollbackPermit load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Approves a rollback to a previously signed firmware revision after a defined failure trigger; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid firmware rollback permit operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
