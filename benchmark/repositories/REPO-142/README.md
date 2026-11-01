# ProofingDecision

Synthetic identity credentials pki trust application for An authorized identity proofing decision records operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/proofing_decision` uses a classical RSA baseline. The separate reference under `migrated_reference/proofing_decision_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic identity proofing decision records service that records, validates, and cryptographically proves identity proofing decision records without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is constrains credential type length and assurance. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_proofing_decision.py -q` and `python -m pytest tests/test_proofing_decision_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
