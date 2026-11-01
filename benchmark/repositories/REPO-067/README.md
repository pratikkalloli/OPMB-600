# LoanDisclosure

Synthetic financial services insurance application for An authorized consumer loan disclosure delivery operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/loan_disclosure` uses a classical RSA baseline. The separate reference under `migrated_reference/loan_disclosure_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic consumer loan disclosure delivery service that records, validates, and cryptographically proves consumer loan disclosure delivery without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is enforces a variant-specific minimum amount and uppercase currency. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_loan_disclosure.py -q` and `python -m pytest tests/test_loan_disclosure_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
