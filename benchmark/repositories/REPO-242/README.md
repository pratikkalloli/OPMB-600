# LineClearanceToken

Issues shift-bound line-clearance attestations after a product changeover and records which supervisor released the line.

Workflow: Changeover checklist, supervisor approval, release token issuance, and later revocation for a production line.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_line_clearance_token.py` and `python -m pytest tests/test_line_clearance_token_pqc.py` from this directory.

## Domain workflow

The original and PQC service layers expose `clear_production_line`. This operation verifies the current signed record, enforces the application's business-specific policy, and records the resulting decision and evidence transactionally.
