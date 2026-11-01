# MarketplacePayout

Synthetic commerce business transactions application for An authorized marketplace seller payout statements operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/marketplace_payout` uses a classical RSA baseline. The separate reference under `migrated_reference/marketplace_payout_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic marketplace seller payout statements service that records, validates, and cryptographically proves marketplace seller payout statements without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is requires region-scoped commerce evidence. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_marketplace_payout.py -q` and `python -m pytest tests/test_marketplace_payout_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
