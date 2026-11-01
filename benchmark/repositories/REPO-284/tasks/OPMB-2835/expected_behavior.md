# Expected behavior

Migrate DeviceRecoveryTicket verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Coordinates recovery of a lost device identity and records invalidation of its previous credentials; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid device recovery ticket operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
