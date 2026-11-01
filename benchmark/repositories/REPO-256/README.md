# FixtureInspectionSchedule

Tracks fixture inspection intervals and blocks production use when inspection evidence is overdue.

Workflow: Tracks fixture inspection intervals and blocks production use when inspection evidence is overdue; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_fixture_inspection_schedule.py` and `python -m pytest tests/test_fixture_inspection_schedule_pqc.py` from this directory.

## Domain workflow

Both the original and PQC services implement `release_fixture_for_inspection`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.
