# RadiologyPeerReview

Synthetic healthcare life sciences application for An authorized radiologist peer review closure operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state..

The original implementation under `src/radiology_peer_review` uses a classical RSA baseline. The separate reference under `migrated_reference/radiology_peer_review_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same A synthetic radiologist peer review closure service that records, validates, and cryptographically proves radiologist peer review closure without using production data. workflow, domain schema, and lifecycle policy.

The domain invariant is enforces the workflow's minimum sequence. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.

Run from this directory using the pinned root environment: `python -m pytest tests/test_radiology_peer_review.py -q` and `python -m pytest tests/test_radiology_peer_review_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.
