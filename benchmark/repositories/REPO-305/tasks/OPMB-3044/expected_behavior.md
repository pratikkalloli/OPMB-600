# Expected behavior

Migrate DemandResponseEnrollment sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Enrolls a customer resource in a demand-response event with capacity and opt-out bounds; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid demand response enrollment operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
