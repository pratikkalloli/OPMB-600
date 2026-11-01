# Expected behavior

Migrate EdgeNodeAttestation sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records measured boot claims and policy evaluation for an edge node before workload placement; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid edge node attestation operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
