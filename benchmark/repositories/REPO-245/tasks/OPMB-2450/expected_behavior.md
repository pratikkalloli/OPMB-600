# Expected behavior

Migrate BatchYieldCertificate apply only an allowed domain lifecycle transition from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Lot closeout, yield reconciliation, quality signoff, certificate publication, and correction through a new revision. semantics.

Valid batch yield operations remain interoperable with the documented PQC format. Invalid state, bad good_units, altered content, wrong keys, and unsupported versions are rejected.
