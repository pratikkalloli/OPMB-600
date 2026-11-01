# Expected behavior

Migrate BatteryDispatchReceipt serialize the verification key in the algorithm format from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records a storage dispatch request, state-of-charge bounds, and metered response; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid battery dispatch receipt operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
