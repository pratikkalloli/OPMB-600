# Expected behavior

Migrate BatchYieldCertificate protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Lot closeout, yield reconciliation, quality signoff, certificate publication, and correction through a new revision. semantics.

Valid batch yield operations remain interoperable with the documented PQC format. Invalid state, bad good_units, altered content, wrong keys, and unsupported versions are rejected.
