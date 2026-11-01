# Expected behavior

Migrate CarbonSoilSample recover an artifact and reject malformed or altered envelopes from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks soil carbon sample custody and lab result for a named plot and sampling depth; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid carbon soil sample operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
