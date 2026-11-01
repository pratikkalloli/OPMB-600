# IdentityAuditBundle

Synthetic identity credentials pki trust application for An authorized identity access audit checkpoints operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/identity_audit_bundle` uses a classical RSA baseline. The separate reference under `migrated_reference/identity_audit_bundle_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic identity access audit checkpoints service that records, validates, and cryptographically proves identity access audit checkpoints without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is rejects assurance levels outside the relying-party range. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_identity_audit_bundle.py -q` and `python -m pytest tests/test_identity_audit_bundle_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
