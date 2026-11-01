# Expected behavior

Migrate MicrocontrollerBuildProof validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records compiler, source revision, and reproducible build digest for a microcontroller image; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid microcontroller build proof operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
