# Expected behavior

Migrate PeeringKeyAgreement apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records partner endpoint identity and key rotation state for a simulated peering link; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid peering key agreement operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
