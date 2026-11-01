# Expected behavior

Migrate PortContainerSeal load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Binds container identity, seal changes, and authorized port custody events; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid port container seal operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
