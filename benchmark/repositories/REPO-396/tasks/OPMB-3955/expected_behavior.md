# Expected behavior

Migrate LivestockMovementCertificate verify a record signature and reject changed records from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Documents a synthetic livestock group movement with origin, destination, and health hold status; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid livestock movement certificate operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
