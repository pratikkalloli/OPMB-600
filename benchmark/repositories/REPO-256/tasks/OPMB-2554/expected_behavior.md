# Expected behavior

Migrate FixtureInspectionSchedule sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks fixture inspection intervals and blocks production use when inspection evidence is overdue; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid fixture inspection schedule operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
