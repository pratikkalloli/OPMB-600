# Expected behavior

Migrate VehicleRecallNotice generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks affected vehicle serial ranges, notification delivery, and repair completion evidence; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid vehicle recall notice operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
