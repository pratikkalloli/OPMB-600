# Expected behavior

Migrate CommunityEnergySettlement generate an application-specific signature key pair from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Settles synthetic community energy credits across participant meter intervals; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid community energy settlement operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
