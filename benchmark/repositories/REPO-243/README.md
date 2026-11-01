# FixtureCalibrationDossier

Stores dimensional calibration observations for production fixtures and blocks release when measured error exceeds the shop tolerance.

Workflow: Fixture identification, technician measurement, tolerance review, calibration certificate signing, and expiration.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_fixture_calibration_dossier.py` and `python -m pytest tests/test_fixture_calibration_dossier_pqc.py` from this directory.
