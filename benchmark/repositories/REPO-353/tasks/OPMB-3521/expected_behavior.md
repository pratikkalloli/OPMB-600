# Expected behavior

Migrate ShippingHazardDeclaration validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records hazardous cargo classification, packaging checks, and carrier acceptance; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid shipping hazard declaration operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
