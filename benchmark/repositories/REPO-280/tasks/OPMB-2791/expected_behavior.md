# Expected behavior

Migrate EmbeddedConfigBundle validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Approves a device-specific configuration bundle with a monotonic revision and rollback policy; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid embedded config bundle operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
