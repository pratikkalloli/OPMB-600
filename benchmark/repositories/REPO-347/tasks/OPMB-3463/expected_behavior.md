# Expected behavior

Migrate RailCrewDutyRelease generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Verifies crew qualification and rest window before releasing a simulated rail duty; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid rail crew duty release operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
