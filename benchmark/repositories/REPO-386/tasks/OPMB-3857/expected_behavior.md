# Expected behavior

Migrate WiFiControllerEnrollment load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Enrolls a wireless controller with site ownership and approved firmware evidence; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid wi fi controller enrollment operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
