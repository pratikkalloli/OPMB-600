# Expected behavior

Migrate CarbonSoilSample serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks soil carbon sample custody and lab result for a named plot and sampling depth; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid carbon soil sample operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
