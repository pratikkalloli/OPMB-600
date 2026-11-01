# Expected behavior

Migrate EmergencyBroadcastAuthorization load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Authorizes an emergency broadcast area, message revision, and expiry; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid emergency broadcast authorization operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
