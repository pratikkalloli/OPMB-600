# SustainabilityClaim

Synthetic commerce business transactions application for An authorized supplier sustainability claim evidence operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/sustainability_claim` uses a classical RSA baseline. The separate reference under `migrated_reference/sustainability_claim_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic supplier sustainability claim evidence service that records, validates, and cryptographically proves supplier sustainability claim evidence without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is rejects zero quantity orders and malformed regions. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_sustainability_claim.py -q` and `python -m pytest tests/test_sustainability_claim_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
