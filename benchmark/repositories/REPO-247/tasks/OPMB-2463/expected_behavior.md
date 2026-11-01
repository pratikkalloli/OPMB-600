# Expected behavior

Migrate CleanroomProcessTicket generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Room readiness, exposure-window capture, contamination review, process release, and incident quarantine. semantics.

Valid cleanroom ticket operations remain interoperable with the documented PQC format. Invalid state, bad particle_count, altered content, wrong keys, and unsupported versions are rejected.
