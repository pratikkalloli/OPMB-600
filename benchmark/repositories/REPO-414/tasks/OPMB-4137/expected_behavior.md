# Expected behavior

Migrate CropInsuranceEvidence load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Assembles synthetic crop loss observations and assessor signoffs for a claim; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid crop insurance evidence operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
