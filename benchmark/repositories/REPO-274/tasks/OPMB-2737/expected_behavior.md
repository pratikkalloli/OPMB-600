# Expected behavior

Migrate DroneFleetCommand load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Authorizes a bounded mission command for a registered drone and records its operator and geofence; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid drone fleet command operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
