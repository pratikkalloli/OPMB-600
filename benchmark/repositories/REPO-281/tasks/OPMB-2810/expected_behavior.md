# Expected behavior

Migrate SmartLockLease apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Issues a time-bounded access lease to a synthetic smart lock and records revocation events; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid smart lock lease operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
