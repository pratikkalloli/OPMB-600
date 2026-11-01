# Expected behavior

Migrate FurnaceCycleWitness sign a scoped domain record with versioned context from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Binds furnace temperature-time evidence to a heat-treatment batch and blocks release when the cycle window is violated; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid furnace cycle witness operations remain interoperable with the documented PQC format. Invalid state, bad event_count, altered content, wrong keys, and unsupported versions are rejected.
