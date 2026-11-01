# Expected behavior

Migrate LineClearanceToken load and validate a serialized verification key from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Changeover checklist, supervisor approval, release token issuance, and later revocation for a production line. semantics.

Valid line clearance operations remain interoperable with the documented PQC format. Invalid state, bad clearance_code, altered content, wrong keys, and unsupported versions are rejected.
