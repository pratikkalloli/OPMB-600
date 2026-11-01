# CleanroomProcessTicket

Records a controlled cleanroom process window and its particle-count reading, allowing release only when the monitored room stays within its qualified limit.

Workflow: Room readiness, exposure-window capture, contamination review, process release, and incident quarantine.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_cleanroom_process_ticket.py` and `python -m pytest tests/test_cleanroom_process_ticket_pqc.py` from this directory.

## Domain workflow

The original and PQC service layers expose `release_cleanroom_window`. This operation verifies the current signed record, enforces the application's business-specific policy, and records the resulting decision and evidence transactionally.
