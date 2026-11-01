# StudentMobility

Synthetic education research application for An authorized student exchange credit transfer operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/student_mobility` uses a classical RSA baseline. The separate reference under `migrated_reference/student_mobility_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic student exchange credit transfer service that records, validates, and cryptographically proves student exchange credit transfer without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is accepts only bounded academic-cycle identifiers. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_student_mobility.py -q` and `python -m pytest tests/test_student_mobility_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
