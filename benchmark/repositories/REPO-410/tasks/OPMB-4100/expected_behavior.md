# Expected behavior

Migrate AquacultureFeedTrace apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Tracks feed batch and ration events for a synthetic aquaculture enclosure; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid aquaculture feed trace operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
