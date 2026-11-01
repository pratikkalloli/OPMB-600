# FederatedClaimMap

Synthetic identity credentials pki trust application for An authorized federated claim mapping approvals operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/federated_claim_map` uses a classical RSA baseline. The separate reference under `migrated_reference/federated_claim_map_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic federated claim mapping approvals service that records, validates, and cryptographically proves federated claim mapping approvals without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is applies minimum assurance before publishing credentials. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_federated_claim_map.py -q` and `python -m pytest tests/test_federated_claim_map_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
