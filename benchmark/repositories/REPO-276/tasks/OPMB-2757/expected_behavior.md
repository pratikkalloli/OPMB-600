# Expected behavior

Migrate DeviceOwnershipTransfer load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Transfers a device between fictional owners while revoking the prior owner's access grant; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid device ownership transfer operations remain interoperable with the documented PQC format. Invalid state, bad authorization_code, altered content, wrong keys, and unsupported versions are rejected.
