# Expected behavior

Migrate GrainMoistureCertificate generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Attests grain moisture measurements and storage acceptance for a harvest lot; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid grain moisture certificate operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
