# Expected behavior

Migrate FeederSwitchingOrder load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Approves a feeder switching sequence with prerequisite checks and operator acknowledgements; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid feeder switching order operations remain interoperable with the documented PQC format. Invalid state, bad review_class, altered content, wrong keys, and unsupported versions are rejected.
