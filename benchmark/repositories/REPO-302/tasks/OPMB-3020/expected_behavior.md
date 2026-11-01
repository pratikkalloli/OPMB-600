# Expected behavior

Migrate RenewableOutputCertificate apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Attests renewable generator output for a defined meter interval and plant identity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid renewable output certificate operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
