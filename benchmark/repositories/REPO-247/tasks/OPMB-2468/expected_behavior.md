# Expected behavior

Migrate CleanroomProcessTicket protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Room readiness, exposure-window capture, contamination review, process release, and incident quarantine. semantics.

Valid cleanroom ticket operations remain interoperable with the documented PQC format. Invalid state, bad particle_count, altered content, wrong keys, and unsupported versions are rejected.
