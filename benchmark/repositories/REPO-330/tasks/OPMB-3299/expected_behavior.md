# Expected behavior

Migrate CommunityEnergySettlement recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Settles synthetic community energy credits across participant meter intervals; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid community energy settlement operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
