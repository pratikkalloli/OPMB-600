# Expected behavior

Migrate ComponentTraceLot load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Receiving inspection, source-lot binding, production consumption, and traceability export. semantics.

Valid component trace operations remain interoperable with the documented PQC format. Invalid state, bad material_digest, altered content, wrong keys, and unsupported versions are rejected.
