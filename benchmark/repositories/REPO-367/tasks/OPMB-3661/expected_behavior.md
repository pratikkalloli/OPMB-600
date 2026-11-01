# Expected behavior

Migrate EdgeCacheInvalidate validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Issues scoped cache invalidation instructions and records acknowledgements from edge nodes; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid edge cache invalidate operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
