# Expected behavior

Migrate OutageRestorationLog sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks restoration milestones and switching approvals for a simulated outage zone; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid outage restoration log operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
