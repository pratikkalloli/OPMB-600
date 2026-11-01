# Expected behavior

Migrate SpectrumGrantLedger load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Records synthetic spectrum grant intervals, geography, and renewal decisions; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid spectrum grant ledger operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
