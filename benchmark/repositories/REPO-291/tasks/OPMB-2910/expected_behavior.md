# Expected behavior

Migrate DeviceTrustRenewal apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Renews device trust after periodic evidence collection and rejects expired attestation windows; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid device trust renewal operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
