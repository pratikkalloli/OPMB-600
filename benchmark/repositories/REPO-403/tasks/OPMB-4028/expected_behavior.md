# Expected behavior

Migrate HarvestBinHandoff protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Tracks harvest bin custody from field collection through packing intake; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid harvest bin handoff operations remain interoperable with the documented PQC format. Invalid state, bad measured_value, altered content, wrong keys, and unsupported versions are rejected.
