# AdverseEventReport

Synthetic healthcare life sciences application for An authorized adverse drug event case reporting operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/adverse_event_report` uses a classical RSA baseline. The separate reference under `migrated_reference/adverse_event_report_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic adverse drug event case reporting service that records, validates, and cryptographically proves adverse drug event case reporting without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is requires purpose-scoped clinical records. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_adverse_event_report.py -q` and `python -m pytest tests/test_adverse_event_report_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
