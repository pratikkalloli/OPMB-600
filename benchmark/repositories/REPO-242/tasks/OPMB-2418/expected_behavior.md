# Expected behavior

Migrate LineClearanceToken protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Changeover checklist, supervisor approval, release token issuance, and later revocation for a production line. semantics.

Valid line clearance operations remain interoperable with the documented PQC format. Invalid state, bad clearance_code, altered content, wrong keys, and unsupported versions are rejected.
