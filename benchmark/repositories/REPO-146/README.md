# CrossBorderIdentity

Synthetic identity credentials pki trust application for An authorized cross-border identity translation attestations operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/cross_border_identity` uses a classical RSA baseline. The separate reference under `migrated_reference/cross_border_identity_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic cross-border identity translation attestations service that records, validates, and cryptographically proves cross-border identity translation attestations without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is requires a credential strength allowed by issuer policy. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_cross_border_identity.py -q` and `python -m pytest tests/test_cross_border_identity_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
