# Expected behavior

Migrate FuelBlendCertificate validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Attests a delivered fuel blend's composition range and supplier batch identity; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid fuel blend certificate operations remain interoperable with the documented PQC format. Invalid state, bad evidence_digest, altered content, wrong keys, and unsupported versions are rejected.
