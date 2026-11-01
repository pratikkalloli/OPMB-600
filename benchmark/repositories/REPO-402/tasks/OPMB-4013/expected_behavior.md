# Expected behavior

Migrate PesticideApplicationLog generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records treatment product, field boundary, dose, weather, and applicator for compliance review; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid pesticide application log operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
